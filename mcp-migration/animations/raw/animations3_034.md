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
animated-background-lines.tsx
import React from 'react';

const AnimatedCTASection = () => {
  const lineWrapperTops = ['top-[10%]', 'top-[30%]', 'top-[50%]', 'top-[70%]', 'top-[90%]'];

  return (
    <>
      <GlobalStylesAndKeyframes />
      {/* Main section container */}
      <section className="relative min-h-screen flex items-center justify-center bg-black text-white font-sans overflow-hidden p-8 sm:p-16">
        {/* Grid Background */}
        <div
          className="absolute inset-0 w-full h-full bg-[linear-gradient(rgba(255,149,0,0.07)_1px,transparent_1px),linear-gradient(90deg,rgba(255,149,0,0.07)_1px,transparent_1px)] bg-[length:50px_50px] animate-[gridMove_20s_linear_infinite] z-0"
        />

        {/* Animated Background Lines */}
        <div className="absolute inset-0 w-full h-full overflow-hidden z-[1]">
          {lineWrapperTops.map((topClass, index) => (
            <div key={index} className={`absolute w-full h-[100px] ${topClass}`}>
              <div className="w-full h-0.5 relative overflow-hidden">
                <div
                  className={`absolute top-0 w-full h-full animate-[lineMove_4s_linear_infinite] ${
                    index % 2 !== 0 ? '[animation-direction:reverse] [animation-delay:2s]' : ''
                  }`}
                  style={{
                    background: 'linear-gradient(90deg, transparent 0%, #ff9500 20%, #ffd700 50%, #ff9500 80%, transparent 100%)',
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Corner Lines - hidden on small screens, visible on md and up */}
        <div className="hidden md:block absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[300px] h-[100px] z-[5]">
          <svg
            className="absolute top-1/2 -translate-y-1/2 left-[-150px] w-[120px] h-[60px] animate-[cornerLineAnimation_6s_linear_infinite]"
            viewBox="0 0 120 60"
            stroke="#ff9500"
            strokeWidth="2"
            fill="none"
            strokeDasharray="50"
          >
            <path d="M120 0 L20 0 Q0 0 0 20 L0 60" />
          </svg>
          <svg
            className="absolute top-1/2 -translate-y-1/2 right-[-150px] w-[120px] h-[60px] transform scale-x-[-1] animate-[cornerLineAnimation_6s_linear_infinite] [animation-delay:3s]"
            viewBox="0 0 120 60"
            stroke="#ff9500"
            strokeWidth="2"
            fill="none"
            strokeDasharray="50"
          >
            <path d="M120 0 L20 0 Q0 0 0 20 L0 60" />
          </svg>
        </div>

        {/* Main Content */}
        <div className="text-center max-w-3xl z-[10] relative">
          <h1 className="text-[clamp(2.5rem,5vw,4rem)] font-bold leading-tight mb-8">
            Ready to build
            <br />
            <span
              className="inline-block animate-[gradientShift_3s_ease-in-out_infinite_alternate]"
              style={{
                backgroundImage: 'linear-gradient(45deg, #ff9500, #ffb347, #ffd700)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                // textFillColor: 'transparent', // Standard property, not fully cross-browser for this effect
              }}
            >
              the software of the future?
            </span>
          </h1>
          <a
            href="#"
            className="inline-block py-3 px-8 sm:py-4 sm:px-10 bg-white text-black no-underline rounded-lg font-semibold text-base sm:text-lg mt-8 transition-all duration-300 ease-in-out hover:-translate-y-0.5 hover:shadow-[0_10px_30px_rgba(255,255,255,0.15)] active:translate-y-0 active:shadow-[0_5px_15px_rgba(255,255,255,0.1)]"
          >
            Start building
          </a>
        </div>
      </section>
    </>
  );
};

// Component to inject global styles and keyframes
const GlobalStylesAndKeyframes = () => (
  <style jsx global>{`
    @keyframes gradientShift {
      0% { filter: hue-rotate(0deg); }
      100% { filter: hue-rotate(30deg); }
    }
    @keyframes lineMove {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
    @keyframes cornerLineAnimation {
      0% { stroke-dashoffset: 0; }
      25% { stroke-dashoffset: 100; }
      50% { stroke-dashoffset: 200; }
      75% { stroke-dashoffset: 300; }
      100% { stroke-dashoffset: 400; }
    }
    @keyframes gridMove {
      0% { background-position: 0 0; }
      100% { background-position: 50px 50px; }
    }
    /* Apply body-level styles to a root wrapper if this component is the whole page */
    /* For example, if you have a div with id="root" where the React app mounts:
    #root {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; // Or rely on Tailwind's font-sans
      background: #000;
      color: white;
      overflow-x: hidden;
    }
    */
  `}</style>
);

export default function CtaPage() {
  return (
    <div className="bg-black"> {/* Added bg-black here to ensure full page background if needed */}
      <AnimatedCTASection />
    </div>
  );
}


demo.tsx
import CtaPage from "@/components/ui/animated-background-lines";

const DemoOne = () => {
  return (
    <div className="w-full h-screen">
      <CtaPage />
    </div>
  );
};

export { DemoOne };

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
