You are given a task to integrate an existing React component in the codebase

~~~/README.md
# FuzzyText Component

A text component that renders a fuzzy/glitchy text effect using HTML5 Canvas. It supports hover effects, click interactions, and continuous glitch modes.

## Usage

```tsx
import { FuzzyText } from '@/sd-components/bf0a7e67-7ecb-4d63-a4bf-83a3064a1235';

function MyComponent() {
  return (
    <FuzzyText 
      fontSize="4rem"
      fontWeight={900}
      color="#fff"
      enableHover={true}
      baseIntensity={0.2}
      hoverIntensity={0.5}
    >
      GLITCH
    </FuzzyText>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | React.ReactNode | - | The text to render. |
| fontSize | number \| string | 'clamp(2rem, 8vw, 8rem)' | Font size of the text. |
| fontWeight | string \| number | 900 | Font weight of the text. |
| fontFamily | string | 'inherit' | Font family. |
| color | string | '#fff' | Text color. |
| enableHover | boolean | true | Whether to enable intensity change on hover. |
| baseIntensity | number | 0.18 | The base amount of fuzziness (0-1 recommended). |
| hoverIntensity | number | 0.5 | The intensity when hovering. |
| fuzzRange | number | 30 | The pixel range of the displacement. |
| fps | number | 60 | Frames per second for the animation. |
| direction | 'horizontal' \| 'vertical' \| 'both' | 'horizontal' | Direction of the fuzzy displacement. |
| transitionDuration | number | 0 | Duration in ms to transition between intensities. |
| clickEffect | boolean | false | Whether to trigger a high intensity burst on click. |
| glitchMode | boolean | false | If true, triggers random glitch bursts automatically. |
| glitchInterval | number | 2000 | Interval between glitches in ms. |
| glitchDuration | number | 200 | Duration of each glitch burst in ms. |
| gradient | string[] \| null | null | Array of colors for gradient text. Overrides color prop. |
| letterSpacing | number | 0 | Letter spacing in pixels. |
| className | string | '' | Additional CSS classes for the canvas element. |
~~~

~~~/src/App.tsx
import React from 'react';
import { FuzzyText } from './Component';
import { RefreshCw } from 'lucide-react';

export default function App() {
  const [key, setKey] = React.useState(0);

  const handleReplay = () => {
    setKey(prev => prev + 1);
  };

  return (
    <div className="relative min-h-screen w-full flex flex-col items-center justify-center bg-[#1A1A1B] p-8 font-sans overflow-hidden">
      
      {/* Container with "floating" premium feel */}
      <div className="relative z-10 p-20 rounded-3xl bg-[#1A1A1B] shadow-[0_0_40px_rgba(0,0,0,0.1)] flex items-center justify-center">
        <div key={key} className="flex flex-col items-center gap-4">
          <FuzzyText 
            fontSize="clamp(3rem, 12vw, 9rem)"
            fontWeight={900}
            fontFamily="inherit"
            color="#FFFFFF"
            enableHover={true}
            baseIntensity={0.15}
            hoverIntensity={0.5}
            fuzzRange={25}
            clickEffect={true}
            transitionDuration={200}
            direction="both"
          >
            FUZZY
          </FuzzyText>
          
          <div className="mt-8 text-neutral-500 text-sm font-medium tracking-widest uppercase opacity-60">
            Interactive Text Effect
          </div>
        </div>
      </div>

      {/* Decorative background elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none opacity-20">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-white/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 bg-white/5 rounded-full blur-3xl" />
      </div>

      {/* Replay Button */}
      <button 
        onClick={handleReplay}
        className="absolute bottom-8 right-8 p-3 rounded-full bg-white/5 hover:bg-white/10 text-white transition-all duration-300 backdrop-blur-sm group"
        aria-label="Replay Animation"
      >
        <RefreshCw className="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" />
      </button>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "fuzzy-text",
  "description": "A text component that renders a fuzzy/glitchy text effect using HTML5 Canvas",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "lucide-react": "^0.292.0"
  }
}
~~~

~~~/src/Component.tsx
import React, { useEffect, useRef } from 'react';

interface FuzzyTextProps {
  children: React.ReactNode;
  fontSize?: number | string;
  fontWeight?: string | number;
  fontFamily?: string;
  color?: string;
  enableHover?: boolean;
  baseIntensity?: number;
  hoverIntensity?: number;
  fuzzRange?: number;
  fps?: number;
  direction?: 'horizontal' | 'vertical' | 'both';
  transitionDuration?: number;
  clickEffect?: boolean;
  glitchMode?: boolean;
  glitchInterval?: number;
  glitchDuration?: number;
  gradient?: string[] | null;
  letterSpacing?: number;
  className?: string;
}

export const FuzzyText: React.FC<FuzzyTextProps> = ({
  children,
  fontSize = 'clamp(2rem, 8vw, 8rem)',
  fontWeight = 900,
  fontFamily = 'inherit',
  color = '#fff',
  enableHover = true,
  baseIntensity = 0.18,
  hoverIntensity = 0.5,
  fuzzRange = 30,
  fps = 60,
  direction = 'horizontal',
  transitionDuration = 0,
  clickEffect = false,
  glitchMode = false,
  glitchInterval = 2000,
  glitchDuration = 200,
  gradient = null,
  letterSpacing = 0,
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement & { cleanupFuzzyText?: () => void }>(null);

  useEffect(() => {
    let animationFrameId: number;
    let isCancelled = false;
    let glitchTimeoutId: ReturnType<typeof setTimeout>;
    let glitchEndTimeoutId: ReturnType<typeof setTimeout>;
    let clickTimeoutId: ReturnType<typeof setTimeout>;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const init = async () => {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const computedFontFamily =
        fontFamily === 'inherit' ? window.getComputedStyle(canvas).fontFamily || 'sans-serif' : fontFamily;
      const fontSizeStr = typeof fontSize === 'number' ? `${fontSize}px` : fontSize;
      const fontString = `${fontWeight} ${fontSizeStr} ${computedFontFamily}`;

      try {
        await document.fonts.load(fontString);
      } catch {
        await document.fonts.ready;
      }

      if (isCancelled) return;

      let numericFontSize: number;
      if (typeof fontSize === 'number') {
        numericFontSize = fontSize;
      } else {
        const temp = document.createElement('span');
        temp.style.fontSize = fontSize;
        document.body.appendChild(temp);
        const computedSize = window.getComputedStyle(temp).fontSize;
        numericFontSize = parseFloat(computedSize);
        document.body.removeChild(temp);
      }

      const text = React.Children.toArray(children).join('');
      const offscreen = document.createElement('canvas');
      const offCtx = offscreen.getContext('2d');
      if (!offCtx) return;

      offCtx.font = `${fontWeight} ${fontSizeStr} ${computedFontFamily}`;
      offCtx.textBaseline = 'alphabetic';

      let totalWidth = 0;
      if (letterSpacing !== 0) {
        for (const char of text) {
          totalWidth += offCtx.measureText(char).width + letterSpacing;
        }
        totalWidth -= letterSpacing;
      } else {
        totalWidth = offCtx.measureText(text).width;
      }

      const metrics = offCtx.measureText(text);
      const actualLeft = metrics.actualBoundingBoxLeft ?? 0;
      const actualRight = letterSpacing !== 0 ? totalWidth : (metrics.actualBoundingBoxRight ?? metrics.width);
      const actualAscent = metrics.actualBoundingBoxAscent ?? numericFontSize;
      const actualDescent = metrics.actualBoundingBoxDescent ?? numericFontSize * 0.2;
      const textBoundingWidth = Math.ceil(letterSpacing !== 0 ? totalWidth : actualLeft + actualRight);
      const tightHeight = Math.ceil(actualAscent + actualDescent);

      const extraWidthBuffer = 10;
      const offscreenWidth = textBoundingWidth + extraWidthBuffer;
      offscreen.width = offscreenWidth;
      offscreen.height = tightHeight;

      const xOffset = extraWidthBuffer / 2;

      offCtx.font = `${fontWeight} ${fontSizeStr} ${computedFontFamily}`;
      offCtx.textBaseline = 'alphabetic';

      if (gradient && Array.isArray(gradient) && gradient.length >= 2) {
        const grad = offCtx.createLinearGradient(0, 0, offscreenWidth, 0);
        gradient.forEach((c, i) => grad.addColorStop(i / (gradient.length - 1), c));
        offCtx.fillStyle = grad;
      } else {
        offCtx.fillStyle = color;
      }

      if (letterSpacing !== 0) {
        let xPos = xOffset;
        for (const char of text) {
          offCtx.fillText(char, xPos, actualAscent);
          xPos += offCtx.measureText(char).width + letterSpacing;
        }
      } else {
        offCtx.fillText(text, xOffset - actualLeft, actualAscent);
      }

      const horizontalMargin = fuzzRange + 20;
      const verticalMargin = direction === 'vertical' || direction === 'both' ? fuzzRange + 10 : 0;
      
      canvas.width = offscreenWidth + horizontalMargin * 2;
      canvas.height = tightHeight + verticalMargin * 2;

      ctx.translate(horizontalMargin, verticalMargin);

      const interactiveLeft = horizontalMargin + xOffset;
      const interactiveTop = verticalMargin;
      const interactiveRight = interactiveLeft + textBoundingWidth;
      const interactiveBottom = interactiveTop + tightHeight;

      let isHovering = false;
      let isClicking = false;
      let isGlitching = false;
      let currentIntensity = baseIntensity;
      let targetIntensity = baseIntensity;
      let lastFrameTime = 0;
      const frameDuration = 1000 / fps;

      const startGlitchLoop = () => {
        if (!glitchMode || isCancelled) return;
        glitchTimeoutId = setTimeout(() => {
          if (isCancelled) return;
          isGlitching = true;
          glitchEndTimeoutId = setTimeout(() => {
            isGlitching = false;
            startGlitchLoop();
          }, glitchDuration);
        }, glitchInterval);
      };

      if (glitchMode) startGlitchLoop();

      const run = (timestamp: number) => {
        if (isCancelled) return;

        if (timestamp - lastFrameTime < frameDuration) {
          animationFrameId = window.requestAnimationFrame(run);
          return;
        }
        lastFrameTime = timestamp;

        ctx.clearRect(-fuzzRange - 20, -fuzzRange - 10, offscreenWidth + 2 * (fuzzRange + 20), tightHeight + 2 * (fuzzRange + 10));

        if (isClicking) {
          targetIntensity = 1;
        } else if (isGlitching) {
          targetIntensity = 1;
        } else if (isHovering) {
          targetIntensity = hoverIntensity;
        } else {
          targetIntensity = baseIntensity;
        }

        if (transitionDuration > 0) {
          const step = (1 / (transitionDuration / frameDuration));
          if (currentIntensity < targetIntensity) {
            currentIntensity = Math.min(currentIntensity + step, targetIntensity);
          } else if (currentIntensity > targetIntensity) {
            currentIntensity = Math.max(currentIntensity - step, targetIntensity);
          }
        } else {
          currentIntensity = targetIntensity;
        }

        for (let j = 0; j < tightHeight; j++) {
          let dx = 0, dy = 0;
          if (direction === 'horizontal' || direction === 'both') {
            dx = Math.floor(currentIntensity * (Math.random() - 0.5) * fuzzRange);
          }
          if (direction === 'vertical' || direction === 'both') {
            dy = Math.floor(currentIntensity * (Math.random() - 0.5) * fuzzRange * 0.5);
          }
          ctx.drawImage(offscreen, 0, j, offscreenWidth, 1, dx, j + dy, offscreenWidth, 1);
        }

        animationFrameId = window.requestAnimationFrame(run);
      };

      animationFrameId = window.requestAnimationFrame(run);

      const isInsideTextArea = (x: number, y: number) =>
        x >= interactiveLeft && x <= interactiveRight && y >= interactiveTop && y <= interactiveBottom;

      const handleMouseMove = (e: MouseEvent) => {
        if (!enableHover) return;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        isHovering = isInsideTextArea(x, y);
      };

      const handleMouseLeave = () => {
        isHovering = false;
      };

      const handleClick = () => {
        if (!clickEffect) return;
        isClicking = true;
        clearTimeout(clickTimeoutId);
        clickTimeoutId = setTimeout(() => {
          isClicking = false;
        }, 150);
      };

      const handleTouchMove = (e: TouchEvent) => {
        if (!enableHover) return;
        e.preventDefault();
        const rect = canvas.getBoundingClientRect();
        const touch = e.touches[0];
        const x = touch.clientX - rect.left;
        const y = touch.clientY - rect.top;
        isHovering = isInsideTextArea(x, y);
      };

      const handleTouchEnd = () => {
        isHovering = false;
      };

      if (enableHover) {
        canvas.addEventListener('mousemove', handleMouseMove);
        canvas.addEventListener('mouseleave', handleMouseLeave);
        canvas.addEventListener('touchmove', handleTouchMove, { passive: false });
        canvas.addEventListener('touchend', handleTouchEnd);
      }

      if (clickEffect) {
        canvas.addEventListener('click', handleClick);
      }

      const cleanup = () => {
        window.cancelAnimationFrame(animationFrameId);
        clearTimeout(glitchTimeoutId);
        clearTimeout(glitchEndTimeoutId);
        clearTimeout(clickTimeoutId);
        if (enableHover) {
          canvas.removeEventListener('mousemove', handleMouseMove);
          canvas.removeEventListener('mouseleave', handleMouseLeave);
          canvas.removeEventListener('touchmove', handleTouchMove);
          canvas.removeEventListener('touchend', handleTouchEnd);
        }
        if (clickEffect) {
          canvas.removeEventListener('click', handleClick);
        }
      };

      canvas.cleanupFuzzyText = cleanup;
    };

    init();

    return () => {
      isCancelled = true;
      window.cancelAnimationFrame(animationFrameId);
      clearTimeout(glitchTimeoutId);
      clearTimeout(glitchEndTimeoutId);
      clearTimeout(clickTimeoutId);
      if (canvas && canvas.cleanupFuzzyText) {
        canvas.cleanupFuzzyText();
      }
    };
  }, [children, fontSize, fontWeight, fontFamily, color, enableHover, baseIntensity, hoverIntensity, fuzzRange, fps, direction, transitionDuration, clickEffect, glitchMode, glitchInterval, glitchDuration, gradient, letterSpacing]);

  return <canvas ref={canvasRef} className={className} />;
};

export default FuzzyText;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
