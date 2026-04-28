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
next-reveal.tsx
'use client';

import { cn } from "@/lib/utils";
import { useState } from 'react';

interface FlipTextProps {
  word?: string;
  className?: string;
}

export default function FlipTextReveal({ word = "DIGITAL REALITY", className = "" }: FlipTextProps) {
  const [key, setKey] = useState(0);

  const replay = () => {
    setKey((prev) => prev + 1);
  };

  return (
    <div className={`flip-container ${className}`}>
      
      <div key={key} className="text-wrapper">
        <h1 className="title" aria-label={word}>
          {word.split("").map((char, i) => (
            <span
              key={`${key}-${i}`}
              className="char"
              style={{ "--index": i } as React.CSSProperties}
            >
              {char === " " ? "\u00A0" : char}
            </span>
          ))}
        </h1>
      </div>

      <button className="replay-button" onClick={replay}>
        <span className="btn-text">Replay Action</span>
      </button>

      <style jsx>{`
        /* --- INVERTED THEME VARIABLES --- */
        .flip-container {
          /* Light Mode (Default): Component is BLACK, Text is WHITE */
          --bg-color: #09090b;      
          --text-color: #ffffff;    
          
          /* Button styling */
          --btn-bg: #27272a;       
          --btn-text: #ffffff;
          --btn-border: #3f3f46;
          --btn-hover: #52525b;
        }

        @media (prefers-color-scheme: dark) {
          .flip-container {
            /* Dark Mode: Component is WHITE, Text is BLACK */
            --bg-color: #ffffff;    
            --text-color: #09090b;  
            
            --btn-bg: #f4f4f5;      
            --btn-text: #18181b;
            --btn-border: #e4e4e7;
            --btn-hover: #d4d4d8;
          }
        }

        /* Manual .dark class override */
        :global(.dark) .flip-container {
          --bg-color: #ffffff;    
          --text-color: #09090b;  
          --btn-bg: #f4f4f5;      
          --btn-text: #18181b;
          --btn-border: #e4e4e7;
          --btn-hover: #d4d4d8;
        }

        /* --- Layout --- */
        .flip-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 4rem 2rem;
          background-color: var(--bg-color); 
          color: var(--text-color);
          border-radius: 16px;
          overflow: hidden;
          min-height: 350px;
          width: 100%;
          transition: background-color 0.4s ease, color 0.4s ease;
          
          /* 3D Stage */
          perspective: 800px; 
          box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1);
        }

        /* --- Typography --- */
        .title {
          font-size: 4.5rem; /* Massive text */
          font-weight: 900;
          margin: 0;
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          line-height: 1;
          text-transform: uppercase; /* Force uppercase for impact */
          letter-spacing: -0.04em;   /* Tight tracking */
          transform-style: preserve-3d;
        }

        /* --- 3D Character Animation --- */
        .char {
          display: inline-block;
          color: var(--text-color);
          transform-origin: bottom center; /* Hinge from bottom */
          
          opacity: 0;
          transform: rotateX(-90deg) translateY(20px);
          
          /* Elastic bounce effect */
          animation: flip-up 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
          animation-delay: calc(0.06s * var(--index));
          will-change: transform, opacity;
        }

        /* --- Button --- */
        .replay-button {
          margin-top: 3.5rem;
          padding: 0.8rem 2rem;
          background-color: var(--btn-bg);
          color: var(--btn-text);
          border: 1px solid var(--btn-border);
          border-radius: 99px;
          font-weight: 600;
          font-size: 0.85rem;
          cursor: pointer;
          transition: all 0.2s ease;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .replay-button:hover {
          background-color: var(--btn-hover);
          transform: scale(1.05);
        }
        
        .replay-button:active {
          transform: scale(0.95);
        }

        /* --- Keyframes --- */
        @keyframes flip-up {
          0% {
            opacity: 0;
            transform: rotateX(-90deg) translateY(40px);
          }
          100% {
            opacity: 1;
            transform: rotateX(0deg) translateY(0);
          }
        }

        /* Responsive Text Sizing */
        @media (max-width: 768px) {
          .title { font-size: 2.5rem; }
        }

        @media (prefers-reduced-motion: reduce) {
          .char {
            opacity: 1 !important;
            transform: none !important;
            animation: none !important;
          }
        }
      `}</style>
    </div>
  );
}


demo.tsx
import FlipTextReveal from "@/components/ui/next-reveal";

export default function DemoOne() {
   return (
    // 1. LIGHT MODE: 'bg-zinc-50' (White Page) -> Component will be Black
    // 2. DARK MODE: 'dark:bg-black' (Black Page) -> Component will be White
    <div className="min-h-screen w-full flex items-center justify-center bg-zinc-50 dark:bg-black p-4 transition-colors duration-300">
      
      <div className="w-full max-w-3xl">
        <FlipTextReveal word="NEXT LEVEL" />
      </div>

    </div>
  );
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
