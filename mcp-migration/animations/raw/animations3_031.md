You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
warp-dialog.tsx
"use client"

import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { AnimatePresence, motion } from "motion/react"

import { cn } from "@/lib/utils"

type WarpDialogContextType = {
  open: boolean
  setOpen: (open: boolean | ((prev: boolean) => boolean)) => void
}

const WarpDialogContext = React.createContext<WarpDialogContextType | null>(
  null,
)

export function useWarpDialogContext() {
  const ctx = React.useContext(WarpDialogContext)
  if (!ctx)
    throw new Error("WarpDialog components must be used inside <WarpDialog>")
  return ctx
}

export function WarpDialog({
  open: openProp,
  onOpenChange: setOpenProp,
  ...props
}: React.ComponentProps<"div"> & {
  open?: boolean
  onOpenChange?: (open: boolean) => void
}) {
  const [_open, _setOpen] = React.useState(false)
  const open = openProp ?? _open

  const setOpen = React.useCallback(
    (value: boolean | ((value: boolean) => boolean)) => {
      const openState = typeof value === "function" ? value(open) : value
      if (setOpenProp) {
        setOpenProp(openState)
      } else {
        _setOpen(openState)
      }
    },
    [setOpenProp, open],
  )

  const contextValue = React.useMemo<WarpDialogContextType>(
    () => ({ open, setOpen }),
    [open, setOpen],
  )

  return (
    <WarpDialogContext.Provider value={contextValue}>
      <div data-slot="dialog" {...props} />
    </WarpDialogContext.Provider>
  )
}

export function WarpDialogTrigger({
  asChild = false,
  ...props
}: React.ComponentProps<"div"> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "div"

  const { setOpen } = useWarpDialogContext()

  return (
    <Comp
      onClick={() => setOpen((prev) => !prev)}
      data-slot="dialog-trigger"
      {...props}
    />
  )
}

function WarpDialogOverlay({
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div
      className={cn(
        "data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 fixed inset-0 z-50 bg-red-500/10",
        className,
      )}
      {...props}
    >
      <WarpAnimations />
    </div>
  )
}

export function WarpDialogContent({
  children,
  className,
  ...props
}: React.ComponentProps<typeof motion.div>) {
  const { open, setOpen } = useWarpDialogContext()

  return (
    <AnimatePresence>
      {open && (
        <div className={cn("absolute")}>
          <WarpDialogOverlay />

          <motion.div
            onClick={() => setOpen((prev) => !prev)}
            className="fixed inset-0 flex items-center justify-center z-[1000]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.35, ease: [0.59, 0, 0.35, 1] }}
            {...props}
          >
            <motion.div
              className="relative flex flex-col items-center justify-center gap-4"
              onClick={(e) => e.stopPropagation()}
              initial={{
                rotateX: -5,
                skewY: -1.5,
                scaleY: 2,
                scaleX: 0.4,
                y: 100,
              }}
              animate={{
                rotateX: 0,
                skewY: 0,
                scaleY: 1,
                scaleX: 1,
                y: 0,
                transition: {
                  duration: 0.35,
                  ease: [0.59, 0, 0.35, 1],
                  y: { type: "spring", visualDuration: 0.7, bounce: 0.2 },
                },
              }}
              exit={{
                rotateX: -5,
                skewY: -1.5,
                scaleY: 2,
                scaleX: 0.4,
                y: 100,
              }}
              transition={{ duration: 0.35, ease: [0.59, 0, 0.35, 1] }}
              style={{
                transformPerspective: 1000,
                originX: 0.5,
                originY: 0,
              }}
            >
              {children}
            </motion.div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}

function WarpAnimations() {
  const enterDuration = 0.5
  const exitDuration = 0.25
  return (
    <>
      <motion.div
        className="absolute rounded-full h-1/2 w-1/2 blur-lg origin-center will-change-transform left-[25%] top-[100%]"
        initial={{
          scale: 0,
          opacity: 1,
          backgroundColor: "hsl(10, 64%, 77%)",
        }}
        animate={{
          scale: 10,
          opacity: 0.2,
          backgroundColor: "hsl(6, 93%, 56%)",
          transition: {
            duration: enterDuration,
            opacity: { duration: enterDuration, ease: "easeInOut" },
          },
        }}
        exit={{
          scale: 0,
          opacity: 1,
          backgroundColor: "hsl(10, 64%, 77%)",
          transition: { duration: exitDuration },
        }}
      />
      <motion.div
        className=" absolute blur-[100px] rounded-full bg-red-500/90 h-full w-full top-[-25%] left-[-50%]"
        initial={{ opacity: 0 }}
        animate={{
          opacity: 0.9,
          transition: {
            duration: enterDuration,
            scale: {
              duration: 15,
              repeat: Infinity,
              repeatType: "loop",
              ease: "easeInOut",
              delay: 0.35,
            },
          },
          scale: [1, 0.7, 1],
        }}
        exit={{
          opacity: 0,
          transition: { duration: exitDuration },
        }}
      />
      <motion.div
        className=" absolute blur-[100px] rounded-full bg-red-500/80 w-full h-full top-[25%] left-[50%]"
        initial={{ opacity: 0 }}
        animate={{
          opacity: 0.9,
          transition: {
            duration: enterDuration,
            scale: {
              duration: 15,
              repeat: Infinity,
              repeatType: "loop",
              ease: "easeInOut",
              delay: 0.35,
            },
          },
          scale: [1, 0.7, 1],
        }}
        exit={{
          opacity: 0,
          transition: { duration: exitDuration },
        }}
      />
    </>
  )
}


demo.tsx
import {   WarpDialog,
  WarpDialogContent,
  WarpDialogTrigger, } from "@/components/ui/warp-dialog";

import { Button } from "@/components/ui/button"


export default function DemoOne() {
  return <div className="w-full h-full relative items-center justify-center flex rounded-2xl overflow-hidden">
      <WarpDialog>
        <WarpDialogTrigger asChild>
          <Button variant="outline">Open Dialog</Button>
        </WarpDialogTrigger>
        <WarpDialogContent>
          <h2 className="text-2xl font-bold mb-6">Welcome to Warp Dialog</h2>
          <div className="flex gap-4 justify-center">
            <Button variant="default">Get Started</Button>
            <Button variant="outline">Learn More</Button>
          </div>
        </WarpDialogContent>
      </WarpDialog>
    </div>;
}

```

Copy-paste these files for dependencies:
```tsx
shadcn/button
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  },
)
Button.displayName = "Button"

export { Button, buttonVariants }

```

Install NPM dependencies:
```bash
motion, @radix-ui/react-slot, class-variance-authority
```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them
