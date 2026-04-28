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
animated-video-on-scroll.tsx
"use client"

import * as React from "react"
import {
  HTMLMotionProps,
  MotionValue,
  Variants,
  motion,
  useMotionTemplate,
  useScroll,
  useTransform,
} from "motion/react"

import { cn } from "@/lib/utils"

interface ContainerScrollContextValue {
  scrollYProgress: MotionValue<number>
}
interface ContainerInsetProps extends HTMLMotionProps<"div"> {
  insetYRange?: [number, number]
  insetXRange?: [number, number]
  roundednessRange?: [number, number]
}
const SPRING_TRANSITION_CONFIG = {
  type: "spring",
  stiffness: 100,
  damping: 16,
  mass: 0.75,
  restDelta: 0.005,
}

const variants: Variants = {
  hidden: {
    filter: "blur(10px)",
    opacity: 0,
  },
  visible: {
    filter: "blur(0px)",
    opacity: 1,
  },
}
const ContainerScrollContext = React.createContext<
  ContainerScrollContextValue | undefined
>(undefined)
function useContainerScrollContext() {
  const context = React.useContext(ContainerScrollContext)
  if (!context) {
    throw new Error(
      "useContainerScrollContext must be used within a ContainerScroll Component"
    )
  }
  return context
}

export const ContainerScroll: React.FC<
  React.HTMLAttributes<HTMLDivElement>
> = ({ children, className, ...props }) => {
  const scrollRef = React.useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: scrollRef,
    offset: ["start center", "end end"],
  })

  return (
    <ContainerScrollContext.Provider value={{ scrollYProgress }}>
      <div
        ref={scrollRef}
        className={cn("relative min-h-svh w-full", className)}
        {...props}
      >
        {children}
      </div>
    </ContainerScrollContext.Provider>
  )
}
ContainerScroll.displayName = "ContainerScroll"
interface ContainerAnimatedProps extends HTMLMotionProps<"div"> {
  inputRange?: number[]
  outputRange?: number[]
}
export const ContainerAnimated = React.forwardRef<
  HTMLDivElement,
  ContainerAnimatedProps
>(
  (
    {
      className,
      transition,
      style,
      inputRange = [0.2, 0.8],
      outputRange = [80, 0],
      ...props
    },
    ref
  ) => {
    const { scrollYProgress } = useContainerScrollContext()
    const y = useTransform(scrollYProgress, inputRange, outputRange)
    return (
      <motion.div
        ref={ref}
        className={cn("", className)}
        variants={variants}
        initial="hidden"
        whileInView={"visible"}
        viewport={{ once: true }}
        style={{ y, ...style }}
        transition={{ ...SPRING_TRANSITION_CONFIG, ...transition }}
        {...props}
      />
    )
  }
)
ContainerAnimated.displayName = "ContainerAnimated"

export const ContainerSticky = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("sticky left-0 top-0 min-h-svh w-full", className)}
      {...props}
    />
  )
})
ContainerSticky.displayName = "ContainerSticky"

export const HeroVideo = React.forwardRef<
  HTMLVideoElement,
  HTMLMotionProps<"video">
>(({ style, className, transition, ...props }, ref) => {
  const { scrollYProgress } = useContainerScrollContext()
  const scale = useTransform(scrollYProgress, [0, 0.8], [0.7, 1])

  return (
    <motion.video
      ref={ref}
      className={cn(
        "relative z-10 size-auto max-h-full max-w-full ",
        className
      )}
      autoPlay
      muted
      loop
      playsInline
      style={{ scale, ...style }}
      {...props}
    />
  )
})
HeroVideo.displayName = "HeroVideo"

export const HeroButton = React.forwardRef<
  HTMLButtonElement,
  HTMLMotionProps<"button">
>(({ className, transition, ...props }, ref) => {
  return (
    <motion.button
      whileHover={{
        scale: 1.015,
      }}
      whileTap={{
        scale: 0.985,
      }}
      ref={ref}
      className={cn(
        "group relative flex w-fit items-center rounded-full border border-[#84cc16] bg-gray-950/10 px-4 py-2 shadow-[0px_4px_24px_#84cc16] transition-colors hover:bg-slate-950/50",
        className
      )}
      {...props}
    />
  )
})
HeroButton.displayName = "HeroButton"

export const ContainerInset = React.forwardRef<
  HTMLDivElement,
  ContainerInsetProps
>(
  (
    {
      className,
      style,
      insetYRange = [45, 0],
      insetXRange = [45, 0],
      roundednessRange = [1000, 16],
      transition,
      ...props
    },
    ref
  ) => {
    const { scrollYProgress } = useContainerScrollContext()

    const insetY = useTransform(scrollYProgress, [0, 0.8], insetYRange)
    const insetX = useTransform(scrollYProgress, [0, 0.8], insetXRange)
    const roundedness = useTransform(scrollYProgress, [0, 1], roundednessRange)

    const clipPath = useMotionTemplate`inset(${insetY}% ${insetX}% ${insetY}% ${insetX}% round ${roundedness}px)`

    return (
      <motion.div
        ref={ref}
        className={cn(
          "relateive pointer-events-none overflow-hidden",
          className
        )}
        style={{
          clipPath,
          ...style,
        }}
        {...props}
      />
    )
  }
)
ContainerInset.displayName = "ContainerInset"


demo.tsx
import { ContainerAnimated,
  ContainerInset,
  ContainerScroll,
  ContainerSticky,
  HeroButton,
  HeroVideo } from "@/components/blocks/animated-video-on-scroll"

  export const HeroVideoDemo = () => {
  return (
    <section>
      <ContainerScroll className="h-[350vh]">
        <ContainerSticky
          style={{
            background:
              "radial-gradient(40% 40% at 50% 20%, #0e19ae 0%, #0b1387 22.92%, #080f67 42.71%, #030526 88.54%)", 
          }}
          className="bg-stone-900 px-6 py-10 text-slate-50"
        >
          <ContainerAnimated className="space-y-4 text-center">
            <h1 className="text-5xl font-medium tracking-tighter  md:text-6xl">
              Scroll & Roll
            </h1>
            <p className="mx-auto max-w-[42ch] opacity-80">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Quae,
              et, distinctio eum impedit nihil ipsum modi.
            </p>
          </ContainerAnimated>

          <ContainerInset className="max-h-[450px] w-auto py-6">
            <HeroVideo
              src="https://videos.pexels.com/video-files/8566672/8566672-uhd_2560_1440_30fps.mp4"
              data-src="https://videos.pexels.com/video-files/8566672/8566672-uhd_2560_1440_30fps.mp4"
            />
          </ContainerInset>
          <ContainerAnimated
            transition={{ delay: 0.4 }}
            outputRange={[-120, 0]}
            inputRange={[0, 0.7]}
            className="mx-auto mt-2 w-fit "
          >
            <HeroButton>Get Started</HeroButton>
          </ContainerAnimated>
        </ContainerSticky>
      </ContainerScroll>
    </section>
  )
}

```

Install NPM dependencies:
```bash
motion
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
