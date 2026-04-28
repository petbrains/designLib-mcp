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
circle-unique-load.tsx
"use client";
import React from "react";
import { PlusIcon } from "lucide-react";

type loadingProps = {
  screenHFull?: boolean;
};

export function Loading({ screenHFull = true }: loadingProps) {
  const [state, setState] = React.useState("_");
  const [loadText, setLoadText] = React.useState("Fetching");

  React.useEffect(() => {
    const interval = setInterval(() => {
      if (state === "_") {
        setState("__");
        setLoadText("Fetching");
      } else if (state === "__") {
        setState(".");
        setLoadText("Loading");
      } else if (state === ".") {
        setState("..");
        setLoadText("Updating");
      } else if (state === "..") {
        setState("...");
        setLoadText("Fixing");
      } else {
        setState("_");
        setLoadText("Fetching");
      }
    }, 400);

    return () => clearInterval(interval);
  }, [state]);

  const getBorderColor = (text: string) => {
    switch (text) {
      case "Fetching":
        return "border-lime-400 text-lime-400";
      case "Loading":
        return "border-sky-400 text-sky-400";
      case "Updating":
        return "border-yellow-400 text-yellow-400";
      case "Fixing":
        return "border-orange-400 text-orange-400";
      default:
        return "border-lime-400 text-lime-400";
    }
  };

  const colorClass = getBorderColor(loadText);

  return (
    <div className={`${screenHFull ? "min-h-screen" : ""} relative flex flex-col items-center justify-center`}>
      <div className={`p-1 border border-dashed rounded-full animate-spin ${colorClass}`}>
        <div className={`w-16 h-16 border-4 border-dashed rounded-full flex justify-center items-center animate-spin ${colorClass}`}>
          <PlusIcon />
        </div>
      </div>

      <p className="text-sm font-bold uppercase tracking-widest text-center mt-2">
        {loadText}
        <span className={`ml-1 ${colorClass}`}>{state}</span>
      </p>
    </div>
  );
}


demo.tsx
import { Loading } from "@/components/ui/circle-unique-load";

export default function DemoOne() {
  return <Loading />;
}

```

Install NPM dependencies:
```bash
lucide-react
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
