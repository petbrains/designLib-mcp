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
gradient-bold-card.tsx
"use client";

import React from "react";

const GradientBlobCard: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="relative w-[200px] h-[250px] rounded-[14px] flex flex-col items-center justify-center
                      shadow-[20px_20px_60px_#bebebe,-20px_-20px_60px_#ffffff] dark:shadow-[20px_20px_60px_#111,-20px_-20px_60px_#222]
                      overflow-hidden">

        {/* Glassy Background */}
        <div className="absolute top-[5px] left-[5px] w-[190px] h-[240px] bg-white/95 dark:bg-black/70 backdrop-blur-[24px]
                        rounded-[10px] outline outline-2 outline-white dark:outline-gray-700 z-10"></div>

        {/* Animated Gradient Blob (same bold colors for light & dark mode) */}
        <div className="absolute top-1/2 left-1/2 w-[150px] h-[150px] rounded-full opacity-100
                        filter blur-[12px] z-0 animate-blob 
                        bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500"></div>

        {/* Inline keyframes animation */}
        <style>
          {`
            @keyframes blob {
              0% {
                transform: translate(-100%, -100%);
              }
              25% {
                transform: translate(0%, -100%);
              }
              50% {
                transform: translate(0%, 0%);
              }
              75% {
                transform: translate(-100%, 0%);
              }
              100% {
                transform: translate(-100%, -100%);
              }
            }

            .animate-blob {
              animation: blob 5s linear infinite;
            }
          `}
        </style>
      </div>
    </div>
  );
};

export default GradientBlobCard;


demo.tsx
import GradientBlobCard from "@/components/ui/gradient-bold-card";

export default function DemoOne() {
  return <GradientBlobCard />;
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
