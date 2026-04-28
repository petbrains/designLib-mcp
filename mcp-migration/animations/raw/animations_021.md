You are given a task to integrate an existing React component in the codebase

~~~/README.md
# TiltedCard

A premium interactive card component with 3D parallax effects, physics-based motion, and a follow-the-cursor tooltip.

## Dependencies
- `framer-motion`: `^11.0.0`
- `lucide-react`: `^0.454.0`
- `clsx`: `^2.1.1`
- `tailwind-merge`: `^2.5.4`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `imageSrc` | `string` | - | **Required**. Source URL for the card image |
| `altText` | `string` | `'Tilted card image'` | Alt text for accessibility |
| `captionText` | `string` | `''` | Text shown in the floating tooltip |
| `containerHeight` | `CSSProperties['height']` | `'300px'` | Height of the outer container |
| `containerWidth` | `CSSProperties['width']` | `'100%'` | Width of the outer container |
| `imageHeight` | `CSSProperties['height']` | `'300px'` | Height of the actual image |
| `imageWidth` | `CSSProperties['width']` | `'300px'` | Width of the actual image |
| `scaleOnHover` | `number` | `1.1` | Scaling factor when hovered |
| `rotateAmplitude` | `number` | `14` | Maximum rotation degrees |
| `showMobileWarning` | `boolean` | `true` | Whether to show a mobile optimization warning |
| `showTooltip` | `boolean` | `true` | Whether to show the cursor tooltip |
| `overlayContent` | `ReactNode` | `null` | Custom content to overlay with Z-depth |
| `displayOverlayContent` | `boolean` | `false` | Whether to display the overlay |
| `className` | `string` | `''` | Additional Tailwind classes |

## Usage

```tsx
import { TiltedCard } from '@/sd-components/83136682-c33a-464b-ad02-7a44fd1b6dcd';

function MyComponent() {
  return (
    <TiltedCard
      imageSrc="https://example.com/image.jpg"
      altText="Description"
      captionText="The Tooltip Text"
      rotateAmplitude={12}
      scaleOnHover={1.15}
      displayOverlayContent={true}
      overlayContent={
        <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
          Overlay Text
        </div>
      }
    />
  );
}
```
~~~

~~~/src/App.tsx
/**
 * TiltedCard Showcase Application
 * 
 * Demonstrates the TiltedCard component in a minimalist environment
 * following the "Minimalist Showcase" design guidelines.
 */

import { TiltedCard } from './Component';

export default function App() {
  return (
    <div className="min-h-screen bg-[#F9F9F9] flex flex-col items-center justify-center p-20 font-sans">
      <div className="flex flex-col items-center gap-12">
        <h1 className="text-2xl font-medium text-[#1A1A1B] tracking-tight">
          Tilted Card Animation
        </h1>
        
        <div className="p-20 bg-white rounded-[40px] shadow-[0_20px_40px_rgba(0,0,0,0.05)] border border-transparent">
          <TiltedCard
            imageSrc="https://i.scdn.co/image/ab67616d0000b273d9985092cd88bffd97653b58"
            altText="Kendrick Lamar - GNX Album Cover"
            captionText="Kendrick Lamar - GNX"
            containerHeight="400px"
            containerWidth="400px"
            imageHeight="300px"
            imageWidth="300px"
            rotateAmplitude={12}
            scaleOnHover={1.2}
            showMobileWarning={false}
            showTooltip={true}
            displayOverlayContent={true}
            overlayContent={
              <div className="bg-black/40 backdrop-blur-md px-4 py-2 rounded-full border border-white/20">
                <p className="text-white text-sm font-medium">
                  GNX
                </p>
              </div>
            }
          />
        </div>
        
        <button 
          onClick={() => window.location.reload()}
          className="px-6 py-2 bg-[#1A1A1B] text-white rounded-full text-sm font-medium transition-all hover:scale-105 active:scale-95 shadow-md"
        >
          Replay
        </button>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "tilted-card-showcase",
  "description": "Premium 3D interactive card showcase",
  "dependencies": {
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.454.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4"
  }
}
~~~

~~~/src/Component.tsx
/**
 * TiltedCard Component
 * 
 * A high-end interactive card that tilts in 3D space based on mouse position.
 * Features:
 * - Smooth physics-based 3D rotation using motion/react
 * - Dynamic tooltip that follows the cursor
 * - Optional overlay content with depth (translateZ)
 * - Configurable scale and rotation amplitude
 */

import type { SpringOptions } from 'framer-motion';
import { useRef, useState } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';

export interface TiltedCardProps {
  /** Source URL for the card image */
  imageSrc: string;
  /** Alt text for the image */
  altText?: string;
  /** Text shown in the floating tooltip */
  captionText?: string;
  /** Height of the outer container */
  containerHeight?: React.CSSProperties['height'];
  /** Width of the outer container */
  containerWidth?: React.CSSProperties['width'];
  /** Height of the actual image */
  imageHeight?: React.CSSProperties['height'];
  /** Width of the actual image */
  imageWidth?: React.CSSProperties['width'];
  /** Scaling factor when hovered (e.g., 1.1) */
  scaleOnHover?: number;
  /** Maximum rotation degrees (higher = more intense tilt) */
  rotateAmplitude?: number;
  /** Whether to show a warning message on mobile devices */
  showMobileWarning?: boolean;
  /** Whether to show the cursor-following tooltip */
  showTooltip?: boolean;
  /** Custom content to overlay on top of the card */
  overlayContent?: React.ReactNode;
  /** Whether to display the overlay content */
  displayOverlayContent?: boolean;
  /** Custom class name for the figure element */
  className?: string;
}

const springValues: SpringOptions = {
  damping: 30,
  stiffness: 100,
  mass: 2
};

export const TiltedCard = ({
  imageSrc,
  altText = 'Tilted card image',
  captionText = '',
  containerHeight = '300px',
  containerWidth = '100%',
  imageHeight = '300px',
  imageWidth = '300px',
  scaleOnHover = 1.1,
  rotateAmplitude = 14,
  showMobileWarning = true,
  showTooltip = true,
  overlayContent = null,
  displayOverlayContent = false,
  className = ''
}: TiltedCardProps) => {
  const ref = useRef<HTMLElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotateX = useSpring(useMotionValue(0), springValues);
  const rotateY = useSpring(useMotionValue(0), springValues);
  const scale = useSpring(1, springValues);
  const opacity = useSpring(0);
  const rotateFigcaption = useSpring(0, {
    stiffness: 350,
    damping: 30,
    mass: 1
  });
  const [lastY, setLastY] = useState(0);

  function handleMouse(e: React.MouseEvent<HTMLElement>) {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const offsetX = e.clientX - rect.left - rect.width / 2;
    const offsetY = e.clientY - rect.top - rect.height / 2;
    
    const rotationX = (offsetY / (rect.height / 2)) * -rotateAmplitude;
    const rotationY = (offsetX / (rect.width / 2)) * rotateAmplitude;
    
    rotateX.set(rotationX);
    rotateY.set(rotationY);
    
    x.set(e.clientX - rect.left);
    y.set(e.clientY - rect.top);
    
    const velocityY = offsetY - lastY;
    rotateFigcaption.set(-velocityY * 0.6);
    setLastY(offsetY);
  }

  function handleMouseEnter() {
    scale.set(scaleOnHover);
    opacity.set(1);
  }

  function handleMouseLeave() {
    opacity.set(0);
    scale.set(1);
    rotateX.set(0);
    rotateY.set(0);
    rotateFigcaption.set(0);
  }

  return (
    <figure
      ref={ref}
      className={`relative w-full h-full [perspective:800px] flex flex-col items-center justify-center ${className}`}
      style={{
        height: containerHeight,
        width: containerWidth
      }}
      onMouseMove={handleMouse}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {showMobileWarning && (
        <div className="absolute top-4 text-center text-sm block sm:hidden text-muted-foreground">
          This effect is optimized for desktop.
        </div>
      )}
      
      <motion.div
        className="relative [transform-style:preserve-3d]"
        style={{
          width: imageWidth,
          height: imageHeight,
          rotateX,
          rotateY,
          scale
        }}
      >
        <motion.img
          src={imageSrc}
          alt={altText}
          className="absolute top-0 left-0 object-cover rounded-[15px] border border-border/50 shadow-2xl will-change-transform [transform:translateZ(0)]"
          style={{
            width: imageWidth,
            height: imageHeight
          }}
        />
        
        {displayOverlayContent && overlayContent && (
          <motion.div className="absolute top-0 left-0 z-[2] w-full h-full flex items-center justify-center will-change-transform [transform:translateZ(30px)] pointer-events-none">
            {overlayContent}
          </motion.div>
        )}
      </motion.div>

      {showTooltip && (
        <motion.figcaption
          className="pointer-events-none absolute left-0 top-0 rounded-[4px] bg-background border border-border px-[10px] py-[4px] text-[10px] text-foreground shadow-lg opacity-0 z-[3] hidden sm:block whitespace-nowrap"
          style={{
            x,
            y,
            opacity,
            rotate: rotateFigcaption
          }}
        >
          {captionText}
        </motion.figcaption>
      )}
    </figure>
  );
};

export default TiltedCard;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
