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
flip-countdown.tsx
// component.tsx
import React, { useState, useEffect, useMemo } from 'react';

// A simple utility for conditional class names
const cn = (...inputs: (string | undefined | null | boolean)[]) =>
  inputs.filter(Boolean).join(' ');

// Internal component for a single digit. No changes needed here.
const FlipUnit = ({
  digit,
  cardStyle,
}: {
  digit: string;
  cardStyle: React.CSSProperties;
}) => {
  const [currentDigit, setCurrentDigit] = useState(digit);
  const [previousDigit, setPreviousDigit] = useState(digit);
  const [isFlipping, setIsFlipping] = useState(false);

  useEffect(() => {
    if (digit !== currentDigit) {
      setPreviousDigit(currentDigit);
      setCurrentDigit(digit);
      setIsFlipping(true);
    }
  }, [digit, currentDigit]);

  const handleAnimationEnd = () => {
    setIsFlipping(false);
    setPreviousDigit(digit);
  };

  return (
    <div className="flip-unit" style={cardStyle}>
      <div className="flip-card flip-card__bottom">{currentDigit}</div>
      <div className="flip-card flip-card__top">{previousDigit}</div>
      <div
        className={cn('flipper', isFlipping && 'is-flipping')}
        onAnimationEnd={handleAnimationEnd}
      >
        <div className="flip-card flipper__top">{previousDigit}</div>
        <div className="flip-card flipper__bottom">{currentDigit}</div>
      </div>
    </div>
  );
};

// Main exported component, now supporting arbitrarily large numbers
export const FlipCountdown = ({
  countFrom = 99,
  countTo = 0,
  className,
  cardBgColor,
  textColor,
}: {
  countFrom?: number | string | bigint;
  countTo?: number | string | bigint;
  className?: string;
  cardBgColor?: string;
  textColor?: string;
}) => {
  // Use BigInt internally for safe handling of large numbers
  const from = useMemo(() => BigInt(countFrom), [countFrom]);
  const to = useMemo(() => BigInt(countTo), [countTo]);

  const isCountingDown = from > to;
  const [count, setCount] = useState(from);

  useEffect(() => {
    // Stop the timer if the target is reached
    if ((isCountingDown && count <= to) || (!isCountingDown && count >= to)) {
      return;
    }

    const timer = setInterval(() => {
      // Use BigInt arithmetic (e.g., 1n)
      setCount((prevCount) => (isCountingDown ? prevCount - 1n : prevCount + 1n));
    }, 1000);

    return () => clearInterval(timer);
  }, [count, to, isCountingDown]);

  // Calculate padding based on the largest number's length
  const paddedCount = useMemo(() => {
    const maxVal = from > to ? from : to;
    const numDigits = String(maxVal).length;
    const displayCount = count < 0n ? 0n : count;
    
    return String(displayCount).padStart(numDigits, '0');
  }, [count, from, to]);

  const cardStyle: React.CSSProperties = {
    '--flip-card-bg': cardBgColor,
    '--flip-card-text': textColor,
  } as React.CSSProperties;

  return (
    <div className={cn('flip-countdown-container', className)}>
      {paddedCount.split('').map((digit, index) => (
        <FlipUnit key={index} digit={digit} cardStyle={cardStyle} />
      ))}
    </div>
  );
};

demo.tsx
import React, { useState } from 'react';
import { FlipCountdown } from "@/components/ui/flip-countdown";

export default function FlipCountdownDemo() {
  const [key, setKey] = useState(0);
  // Use strings for state to accommodate large numbers from input fields
  const [countFrom, setCountFrom] = useState('100');
  const [countTo, setCountTo] = useState('0');

  const restartCountdown = () => {
    // A non-empty value is required for the component to render
    if (countFrom.trim() === '' || countTo.trim() === '') {
        alert("Please enter a 'From' and 'To' value.");
        return;
    }
    setKey(prevKey => prevKey + 1);
  };

  // Restrict input to only digits
  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>, 
    setter: React.Dispatch<React.SetStateAction<string>>
  ) => {
    const value = e.target.value.replace(/[^0-9]/g, '');
    setter(value);
  }

  return (
    <div className="flex flex-col items-center gap-8 p-4">
      
      {/* The component now accepts string props for large numbers */}
      <FlipCountdown 
        key={key} 
        countFrom={countFrom} 
        countTo={countTo} 
      />

      <div className="flex flex-wrap items-center justify-center gap-4">
        <div className="flex flex-col gap-1.5">
            <label htmlFor="from" className="text-sm font-medium text-muted-foreground">From</label>
            <input 
                id="from"
                type="text" // Use text to allow for very large numbers
                inputMode="numeric" // Helps mobile users get a number pad
                value={countFrom}
                onChange={(e) => handleInputChange(e, setCountFrom)}
                className="w-32 rounded-md border bg-transparent p-2 text-center"
                placeholder="e.g., 10000"
            />
        </div>

        <div className="flex flex-col gap-1.5">
            <label htmlFor="to" className="text-sm font-medium text-muted-foreground">To</label>
            <input 
                id="to"
                type="text"
                inputMode="numeric"
                value={countTo}
                onChange={(e) => handleInputChange(e, setCountTo)}
                className="w-32 rounded-md border bg-transparent p-2 text-center"
                placeholder="e.g., 0"
            />
        </div>
        
        <button
          onClick={restartCountdown}
          className="self-end rounded-md bg-primary px-4 py-2 text-primary-foreground transition-colors hover:bg-primary/90"
        >
          Restart
        </button>
      </div>
    </div>
  );
}
```

Extend existing Tailwind 4 index.css with this code (or if project uses Tailwind 3, extend tailwind.config.js or globals.css):
```css
@import "tailwindcss";
@import "tw-animate-css";


@keyframes flip-top {
  100% {
    transform: rotateX(-180deg);
  }
}

@keyframes flip-bottom {
  100% {
    transform: rotateX(0deg);
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
