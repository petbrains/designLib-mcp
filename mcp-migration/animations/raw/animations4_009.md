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
animated-svg-text-path.tsx
import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';

type AnimatedTextPathProps = {
  text?: string;
  duration?: number;
  reversed?: boolean;
  fontSize?: string;
  letterSpacing?: string;
  svgPath?: string;
  viewBox?: string;
  rotation?: number;
  className?: string;
};

const AnimatedTextPath: React.FC<AnimatedTextPathProps> = ({
  text = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do",
  duration = 21,
  reversed = false,
  fontSize = "17px",
  letterSpacing = "-0.47px",
  svgPath = "M227 120C227 142.091 178.871 160 119.5 160C60.1294 160 12 142.091 12 120C12 97.9086 60.1294 80 119.5 80C178.871 80 227 97.9086 227 120Z", 
  viewBox = "0 0 240 240",
  rotation = -40,
  className = ""
}) => {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const animationRef = useRef<any>(null);

  useEffect(() => {
    const loadGSAP = async () => {
      if (typeof window !== 'undefined' && !window.gsap) {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js';
        script.onload = () => initAnimation();
        document.head.appendChild(script);
      } else if (window.gsap) {
        initAnimation();
      }
    };

    const initAnimation = () => {
      const { gsap } = window as any;
      const svg = svgRef.current;
      if (!svg || !gsap) return;

      if (animationRef.current) {
        animationRef.current.kill();
      }

      const pathId = `path-${Math.floor(Math.random() * 900000) + 100000}`;
      const path = svg.querySelector('path');

      if (path) {
        gsap.set(path, {
          attr: {
            fill: "none",
            id: pathId,
            stroke: "none"
          }
        });
      }

      const existingTexts = svg.querySelectorAll('text');
      existingTexts.forEach(el => el.remove());

      const textElement = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      textElement.innerHTML = `
        <textPath href="#${pathId}" startOffset="0%">${text}</textPath>
        <textPath href="#${pathId}" startOffset="0%">${text}</textPath>
      `;
      svg.appendChild(textElement);

      const textPaths = svg.querySelectorAll('textPath');
      gsap.set(textPaths, {
        fontSize: /iPhone/.test(navigator.userAgent) ? "19px" : fontSize,
        letterSpacing: letterSpacing,
        fill: "currentColor"
      });

      const props = {
        duration,
        ease: "none",
        repeat: -1
      };

      const tl = gsap.timeline();
      animationRef.current = tl;

      tl.fromTo(
        textPaths[0],
        { attr: { startOffset: "0%" } },
        { attr: { startOffset: reversed ? "-100%" : "100%" }, ...props },
        0
      );

      tl.fromTo(
        textPaths[1],
        { attr: { startOffset: reversed ? "100%" : "-100%" } },
        { attr: { startOffset: "0%" }, ...props },
        0
      );
    };

    loadGSAP();

    return () => {
      if (animationRef.current) {
        animationRef.current.kill();
      }
    };
  }, [text, duration, reversed, fontSize, letterSpacing, svgPath]);

  return (
    <div className={`flex flex-col items-center justify-center min-h-screen overflow-hidden text-foreground font-sans ${className}`}>
      <div className="w-[min(95vw,95vh)]">
        <svg
          ref={svgRef}
          viewBox={viewBox}
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full"
          style={{ 
            transform: `rotate(${rotation}deg)`,
            backgroundColor: 'transparent'
          }}
        >
          <path d={svgPath} fill="none" />
        </svg>
      </div>
    </div>
  );
};

export { AnimatedTextPath };

demo.tsx
import { AnimatedTextPath } from "@/components/ui/animated-svg-text-path";

const DemoOne = () => {
  return (
     <AnimatedTextPath
        text="looping SVG Text Path. Any Shape And it Still Animates In Any Path."
        duration={18}
        reversed={false}
        fontSize="16px"
        letterSpacing="0.2px"
        rotation={40}
      />
  )
  ;
};

const DemoTwo = () => {
  return (
     <AnimatedTextPath
        text="looping SVG path . Make any shape You want and add text to it ."
        duration={18}
        reversed={false}
        fontSize="16px"
        letterSpacing="0.2px"
        rotation={20}
        svgPath="M 80 110 C 80 50, 130 50, 140 110 C 150 170, 200 170, 200 110 C 200 50, 150 50, 140 110 C 130 170, 80 170, 80 110"
      />
  )
  ;
};

export { DemoOne, DemoTwo };

```

Install NPM dependencies:
```bash
gsap
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
