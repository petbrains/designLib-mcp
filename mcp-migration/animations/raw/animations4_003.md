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
animated-input.tsx
"use client"

import React, { useEffect, useMemo, useRef, useState } from "react"

export function OrbInput() {
  const [value, setValue] = useState("")
  const [isFocused, setIsFocused] = useState(false)
  const [placeholderIndex, setPlaceholderIndex] = useState(0)
  const [displayedText, setDisplayedText] = useState("")
  const [isTyping, setIsTyping] = useState(true)

  // Keep the placeholders stable across renders
  const placeholders = useMemo(
    () => [
      "Ask anything...",
      "What's on your mind?",
      "How can I help you?",
      "What would you like to know?",
    ],
    []
  )

  // Config: tweak the animation to taste
  const CHAR_DELAY = 75 // ms between characters while typing
  const IDLE_DELAY_AFTER_FINISH = 2200 // ms to wait after a full sentence is shown

  // Refs to hold active timers so they can be cleaned up
  const intervalRef = useRef(null)
  const timeoutRef = useRef(null)

  useEffect(() => {
    // clear any stale timers (helps with StrictMode double-invoke in dev)
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
      timeoutRef.current = null
    }

    const current = placeholders[placeholderIndex]
    if (!current) {
      setDisplayedText("")
      setIsTyping(false)
      return
    }

    const chars = Array.from(current)

    // reset state for a new round
    setDisplayedText("")
    setIsTyping(true)

    let charIndex = 0

    // type character-by-character using a derived slice to avoid any chance of appending undefined
    intervalRef.current = window.setInterval(() => {
      if (charIndex < chars.length) {
        const next = chars.slice(0, charIndex + 1).join("")
        setDisplayedText(next)
        charIndex += 1
      } else {
        if (intervalRef.current) {
          clearInterval(intervalRef.current)
          intervalRef.current = null
        }
        setIsTyping(false)

        // after a brief pause, advance to the next placeholder
        timeoutRef.current = window.setTimeout(() => {
          setPlaceholderIndex((prev) => (prev + 1) % placeholders.length)
        }, IDLE_DELAY_AFTER_FINISH)
      }
    }, CHAR_DELAY)

    // Cleanup on unmount or when placeholderIndex changes
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
        timeoutRef.current = null
      }
    }
  }, [placeholderIndex, placeholders])

  return (
    <div className="relative">
      <div
        className={`flex items-center gap-4 p-6 bg-black shadow-lg transition-all duration-300 ease-out rounded-full border border-gray-300 ${
          isFocused ? "shadow-xl scale-[1.02] border-gray-600" : "shadow-lg"
        }`}
      >
        <div className="relative flex-shrink-0">
          <div className="w-16 h-16 rounded-full overflow-hidden transition-all duration-300 scale-100">
            <img
              src="https://media.giphy.com/media/26gsuUjoEBmLrNBxC/giphy.gif"
              alt="Animated orb"
              className="w-full h-full object-cover"
            />
          </div>
        </div>

        <div className="w-px h-12 bg-gray-600" />

        <div className="flex-1 w-[500px]">
          <input
            data-testid="orb-input"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={`${displayedText}${isTyping ? "|" : ""}`}
            aria-label="Ask a question"
            className="w-full text-xl text-white placeholder-gray-400 bg-transparent border-none outline-none font-light"
          />
        </div>
      </div>
    </div>
  )
}

export default OrbInput

demo.tsx
import { OrbInput } from "@/components/ui/animated-input";

export default function DemoOne() {
  return <OrbInput />;
}

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
