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
animated-card.tsx
import React from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";
import { cn } from "@/lib/utils"; // Your utility for merging class names

// --- PROPS INTERFACE ---
export interface JobCardProps {
  companyLogo: React.ReactNode;
  companyName: string;
  jobTitle: string;
  salary: string;
  tags: string[];
  postedDate: string;
  variant?: "pink" | "yellow" | "blue" | "purple";
  className?: string;
  onClick?: () => void;
}

// --- BORDER VARIANT STYLES ---
const variantClasses = {
  pink: "border-t-pink-500",
  yellow: "border-t-yellow-500",
  blue: "border-t-blue-500",
  purple: "border-t-purple-500",
};

/**
 * A responsive, theme-adaptive job card with a 3D tilt effect on hover.
 */
export const AnimatedJobCard = ({
  companyLogo,
  companyName,
  jobTitle,
  salary,
  tags,
  postedDate,
  variant = "purple",
  className,
  onClick,
}: JobCardProps) => {
  // --- FULL ANIMATION LOGIC ---
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const cardRef = React.useRef<HTMLDivElement>(null);

  const onMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const { left, top, width, height } = cardRef.current.getBoundingClientRect();
    mouseX.set(e.clientX - left - width / 2);
    mouseY.set(e.clientY - top - height / 2);
  };

  const onMouseLeave = () => {
    mouseX.set(0);
    mouseY.set(0);
  };

  // Transform mouse position into a 3D rotation (These lines were missing)
  const rotateX = useTransform(mouseY, [-150, 150], [10, -10]);
  const rotateY = useTransform(mouseX, [-150, 150], [-10, 10]);

  // Apply spring physics for a smooth return effect
  const springConfig = { stiffness: 300, damping: 20, mass: 0.5 };
  const springRotateX = useSpring(rotateX, springConfig);
  const springRotateY = useSpring(rotateY, springConfig);

  return (
    <motion.div
      layout
      onClick={onClick}
      transition={{ type: "spring", stiffness: 400, damping: 30 }}
      ref={cardRef}
      onMouseMove={onMouseMove}
      onMouseLeave={onMouseLeave}
      style={{
        rotateX: springRotateX,
        rotateY: springRotateY,
        transformStyle: "preserve-3d",
      }}
      className={cn(
        "relative w-full max-w-sm shrink-0 transform-gpu cursor-pointer overflow-hidden rounded-xl bg-card p-6 shadow-md transition-shadow duration-300 hover:shadow-2xl",
        "border-t-4",
        variantClasses[variant],
        className
      )}
      aria-label={`Job opening: ${jobTitle} at ${companyName}`}
      tabIndex={0}
    >
      <div style={{ transform: "translateZ(20px)" }} className="space-y-4">
        {/* Header */}
        <div className="flex items-center space-x-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted">
            {companyLogo}
          </div>
          <span className="font-semibold text-muted-foreground">{companyName}</span>
        </div>

        {/* Job Details */}
        <div>
          <h3 className="text-lg font-bold text-card-foreground">{jobTitle}</h3>
          <p className="text-sm text-primary">{salary}</p>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Footer */}
        <div className="pt-2 text-right text-xs text-muted-foreground">
          {postedDate}
        </div>
      </div>
    </motion.div>
  );
};

demo.tsx
import React, { useState } from "react";
import { AnimatedJobCard, JobCardProps } from "@/components/ui/animated-card";
import { cn } from "@/lib/utils";

// --- SVG ICONS FOR DEMO ---
const SlackIcon = () => (
  <svg viewBox="0 0 2447.6 2452.5"><g clip-rule="evenodd" fill-rule="evenodd"><path d="m897.4 0c-135.3.1-244.8 109.9-244.7 245.2-.1 135.3 109.5 245.1 244.8 245.2h244.8v-245.1c.1-135.3-109.5-245.1-244.9-245.3.1 0 .1 0 0 0m0 654h-652.6c-135.3.1-244.9 109.9-244.8 245.2-.2 135.3 109.4 245.1 244.7 245.3h652.7c135.3-.1 244.9-109.9 244.8-245.2.1-135.4-109.5-245.2-244.8-245.3z" fill="#36c5f0"/><path d="m2447.6 899.2c.1-135.3-109.5-245.1-244.8-245.2-135.3.1-244.9 109.9-244.8 245.2v245.3h244.8c135.3-.1 244.9-109.9 244.8-245.3zm-652.7 0v-654c.1-135.2-109.4-245-244.7-245.2-135.3.1-244.9 109.9-244.8 245.2v654c-.2 135.3 109.4 245.1 244.7 245.3 135.3-.1 244.9-109.9 244.8-245.3z" fill="#2eb67d"/><path d="m1550.1 2452.5c135.3-.1 244.9-109.9 244.8-245.2.1-135.3-109.5-245.1-244.8-245.2h-244.8v245.2c-.1 135.2 109.5 245 244.8 245.2zm0-654.1h652.7c135.3-.1 244.9-109.9 244.8-245.2.2-135.3-109.4-245.1-244.7-245.3h-652.7c-135.3.1-244.9 109.9-244.8 245.2-.1 135.4 109.4 245.2 244.7 245.3z" fill="#ecb22e"/><path d="m0 1553.2c-.1 135.3 109.5 245.1 244.8 245.2 135.3-.1 244.9-109.9 244.8-245.2v-245.2h-244.8c-135.3.1-244.9 109.9-244.8 245.2zm652.7 0v654c-.2 135.3 109.4 245.1 244.7 245.3 135.3-.1 244.9-109.9 244.8-245.2v-653.9c.2-135.3-109.4-245.1-244.7-245.3-135.4 0-244.9 109.8-244.8 245.1 0 0 0 .1 0 0" fill="#e01e5a"/></g></svg>
);

const GoogleIcon = () => (
  <svg viewBox="0 0 256 262" preserveAspectRatio="xMidYMid"><path d="M255.878 133.451c0-10.734-.871-18.567-2.756-26.69H130.55v48.448h71.947c-1.45 12.04-9.283 30.172-26.69 42.356l-.244 1.622 38.755 30.023 2.685.268c24.659-22.774 38.875-56.282 38.875-96.027" fill="#4285F4"/><path d="M130.55 261.1c35.248 0 64.839-11.605 86.453-31.622l-41.196-31.913c-11.024 7.688-25.82 13.055-45.257 13.055-34.523 0-63.824-22.773-74.269-54.25l-1.531.13-40.298 31.187-.527 1.465C35.393 231.798 79.49 261.1 130.55 261.1" fill="#34A853"/><path d="M56.281 156.37c-2.756-8.123-4.351-16.827-4.351-25.82 0-8.994 1.595-17.697 4.206-25.82l-.073-1.73L15.26 71.312l-1.335.635C5.077 89.644 0 109.517 0 130.55s5.077 40.905 13.925 58.602l42.356-32.782" fill="#FBBC05"/><path d="M130.55 50.479c24.514 0 41.05 10.589 50.479 19.438l36.844-35.974C195.245 12.91 165.798 0 130.55 0 79.49 0 35.393 29.301 13.925 71.947l42.211 32.783c10.59-31.477 39.891-54.251 74.414-54.251" fill="#EB4335"/></svg>
);

// --- INITIAL DEMO DATA ---
const initialJobs: JobCardProps[] = [
  {
    companyLogo: <SlackIcon />,
    companyName: "Slack",
    jobTitle: "Senior UI Designer",
    salary: "$3,500-5,500 net",
    tags: ["Project Based", "Remote"],
    postedDate: "Posted 2 Day Ago",
    variant: "pink",
  },
  {
    companyLogo: <GoogleIcon />,
    companyName: "Google",
    jobTitle: "Lead UX Designer",
    salary: "$4,000-6,000 net",
    tags: ["Full Time", "B2B"],
    postedDate: "Posted Yesterday",
    variant: "yellow",
  },
  {
    companyLogo: <SlackIcon />,
    companyName: "Slack",
    jobTitle: "Lead Product Designer",
    salary: "$3,500-5,500 net",
    tags: ["Full Time", "Remote"],
    postedDate: "Posted 2 Day Ago",
    variant: "blue",
  },
];

// --- DEMO COMPONENT ---
export default function AnimatedJobCardDemo() {
  const [cards, setCards] = useState(initialJobs);

  const cardTransforms = [
    "rotate-[-8deg] translate-x-[-30%] translate-y-[10%] z-0",
    "rotate-[0deg] translate-y-[-5%] z-20",
    "rotate-[8deg] translate-x-[30%] translate-y-[10%] z-10",
  ];

  const handleCardClick = (index: number) => {
    if (index === 1) return;
    const newCards = [...cards];
    const clickedCard = newCards.splice(index, 1)[0];
    newCards.splice(1, 0, clickedCard);
    setCards(newCards);
  };

  return (
    <div className="relative flex h-[500px] w-full items-center justify-center bg-background">
      <div className="relative h-full w-full" style={{ perspective: "1000px" }}>
        {cards.map((job, index) => (
          <AnimatedJobCard
            key={job.jobTitle + job.companyName}
            {...job}
            onClick={() => handleCardClick(index)}
            className={cn(
              "absolute left-0 right-0 top-1/4 mx-auto",
              "w-96",
              cardTransforms[index]
            )}
          />
        ))}
      </div>
    </div>
  );
}
```

Install NPM dependencies:
```bash
framer-motion
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
