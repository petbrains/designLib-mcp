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
3-dots-loader.tsx
import { cn } from "@/lib/utils";
import { useState } from "react";

export const Component = () => {
  const [count, setCount] = useState(0);

  return (
    <>
<div class="container">
  <div class="dot dot-1"></div>
  <div class="dot dot-2"></div>
  <div class="dot dot-3"></div>
</div>

<svg version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="goo">
      <feGaussianBlur
        result="blur"
        stdDeviation="10"
        in="SourceGraphic"
      ></feGaussianBlur>
      <feColorMatrix
        values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 21 -7"
        mode="matrix"
        in="blur"
      ></feColorMatrix>
    </filter>
  </defs>
</svg>
</>
  );
};


demo.tsx
import { Component } from "@/components/ui/3-dots-loader";

export default function DemoOne() {
  return <Component />;
}

```

Extend existing Tailwind 4 index.css with this code (or if project uses Tailwind 3, extend tailwind.config.js or globals.css):
```css
@import "tailwindcss";
@import "tw-animate-css";


@keyframes dot-3-move {
  20% {
    transform: scale(1);
  }
  45% {
    transform: translateY(-18px) scale(0.45);
  }
  60% {
    transform: translateY(-90px) scale(0.45);
  }
  80% {
    transform: translateY(-90px) scale(0.45);
  }
  100% {
    transform: translateY(0px) scale(1);
  }
}

@keyframes dot-2-move {
  20% {
    transform: scale(1);
  }
  45% {
    transform: translate(-16px, 12px) scale(0.45);
  }
  60% {
    transform: translate(-80px, 60px) scale(0.45);
  }
  80% {
    transform: translate(-80px, 60px) scale(0.45);
  }
  100% {
    transform: translateY(0px) scale(1);
  }
}

@keyframes dot-1-move {
  20% {
    transform: scale(1);
  }
  45% {
    transform: translate(16px, 12px) scale(0.45);
  }
  60% {
    transform: translate(80px, 60px) scale(0.45);
  }
  80% {
    transform: translate(80px, 60px) scale(0.45);
  }
  100% {
    transform: translateY(0px) scale(1);
  }
}

@keyframes rotate-move {
  55% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  80% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes index {
  0%,
  100% {
    z-index: 3;
  }
  33.3% {
    z-index: 2;
  }
  66.6% {
    z-index: 1;
  }
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
