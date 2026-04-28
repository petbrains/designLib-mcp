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
3d-card-1.tsx
'use client';

import { motion, useMotionValue, useTransform } from 'framer-motion';
import { Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';

const ROTATION_RANGE = 5;
const PERSPECTIVE = 400;
const INITIAL_DELAY = 0.2;
const CARD_ANIMATION_DURATION = 0.5;

const fadeInVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

const springTransition = {
  type: 'spring',
  stiffness: 100,
  damping: 30,
};

export const Component = () => {
  const [isVisible, setIsVisible] = useState(false);
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const rotateX = useTransform(y, [-50, 50], [ROTATION_RANGE, -ROTATION_RANGE]);
  const rotateY = useTransform(x, [-50, 50], [-ROTATION_RANGE, ROTATION_RANGE]);

  const cardData = {
    number: '4111 1111 1111 9743',
    holder: 'John Doe',
    expiry: '12/24',
  };

  const handleMove = (
    clientX: number,
    clientY: number,
    currentTarget: HTMLElement,
  ) => {
    const rect = currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set(clientX - centerX);
    y.set(clientY - centerY);
  };

  const handleMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
    handleMove(event.clientX, event.clientY, event.currentTarget);
  };

  const handleTouchMove = (event: React.TouchEvent<HTMLDivElement>) => {
    event.preventDefault();
    const touch = event.touches[0];
    handleMove(touch.clientX, touch.clientY, event.currentTarget);
  };

  const handleLeave = () => {
    x.set(0);
    y.set(0);
  };

  const getMaskedNumber = (number: string) => {
    const lastFour = number.slice(-4);
    return `**** **** **** ${lastFour}`;
  };

  return (
    <div className="flex items-center justify-center p-8">
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeInVariants}
        transition={{ duration: CARD_ANIMATION_DURATION }}
        onMouseMove={handleMouseMove}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleLeave}
        onMouseLeave={handleLeave}
        style={{ perspective: PERSPECTIVE }}
        className="relative touch-none"
      >
        <motion.div style={{ rotateX, rotateY }} transition={springTransition}>
          <motion.div
            className="relative h-48 w-80 overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-400 to-cyan-400 p-6 shadow-2xl"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: CARD_ANIMATION_DURATION }}
          >
            <div className="flex items-center justify-between">
              <motion.div
                className="flex items-center space-x-2 text-2xl font-bold text-white"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{
                  delay: INITIAL_DELAY,
                  duration: CARD_ANIMATION_DURATION,
                }}
              >
                <span>VISA</span>
              </motion.div>

              <motion.button
                className="flex h-10 w-10 items-center justify-center rounded-full bg-white/20 text-white backdrop-blur-xs transition-colors hover:bg-white/30"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.4, ...springTransition }}
                onClick={() => setIsVisible(!isVisible)}
                aria-label={
                  isVisible ? 'Hide card details' : 'Show card details'
                }
              >
                {isVisible ? (
                  <EyeOff className="h-5 w-5" />
                ) : (
                  <Eye className="h-5 w-5" />
                )}
              </motion.button>
            </div>

            <motion.div
              className="mt-2 text-xl font-medium tracking-wider text-white"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              {isVisible ? cardData.number : getMaskedNumber(cardData.number)}
            </motion.div>

            <div className="mt-2 flex justify-between text-white">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8, duration: CARD_ANIMATION_DURATION }}
              >
                <div className="text-sm opacity-80">Card Holder</div>
                <div className="font-medium">{cardData.holder}</div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1, duration: CARD_ANIMATION_DURATION }}
              >
                <div className="text-sm opacity-80">Expires</div>
                <div className="font-medium">
                  {isVisible ? cardData.expiry : '**/**'}
                </div>
              </motion.div>
            </div>
          </motion.div>
        </motion.div>
      </motion.div>
    </div>
  );
};

demo.tsx
import { Component } from '@/components/ui/3d-card-1';

const DemoCreditCard = () => {
  return (
    <div className="flex w-full h-screen justify-center items-center bg-muted">
      <Component />
    </div>
  );
};

export default DemoCreditCard;
```

Install NPM dependencies:
```bash
lucide-react, framer-motion
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
