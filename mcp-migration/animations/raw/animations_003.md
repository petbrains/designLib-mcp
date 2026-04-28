You are given a task to integrate an existing React component in the codebase

~~~/README.md
# LetterGlitchBackground

A high-end, minimalist canvas-based background effect that renders a grid of glitching characters. Supports smooth color transitions, custom color palettes, and vignette effects.

## Dependencies
- react: ^18.0.0
- lucide-react: ^0.454.0

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `glitchColors` | `string[]` | `['#2b4539', '#61dca3', '#61b3dc']` | Array of hex colors for the glitching letters |
| `glitchSpeed` | `number` | `50` | Interval in milliseconds between glitch updates |
| `centerVignette` | `boolean` | `false` | Whether to show a dark vignette from the center outwards |
| `outerVignette` | `boolean` | `true` | Whether to show a dark vignette from the edges inwards |
| `smooth` | `boolean` | `true` | Enable smooth color interpolation for transitions |
| `characters` | `string` | `'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$&*()-_+=/[]{};:<>.,0123456789'` | The set of characters to use |
| `className` | `string` | `undefined` | CSS class name for the wrapper |

## Usage
```tsx
import { LetterGlitch } from '@/sd-components/aaa8e7ed-dafe-44e5-8644-e1285b0cee7a';

function MyPage() {
  return (
    <div className="w-full h-screen">
      <LetterGlitch
        glitchSpeed={50}
        centerVignette={true}
        outerVignette={false}
        smooth={true}
      />
    </div>
  );
}
```
~~~

~~~/src/App.tsx
import React, { useState } from 'react';
import { LetterGlitch } from './Component';
import { RotateCcw } from 'lucide-react';

/**
 * App component showcasing the LetterGlitch effect in a minimalist, premium layout.
 */
export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="w-full h-screen bg-background flex flex-col items-center justify-center p-20">
      {/* Floating container with subtle shadow for premium feel */}
      <div 
        key={refreshKey}
        className="relative w-full h-full max-w-5xl rounded-3xl overflow-hidden shadow-[0_40px_80px_-20px_rgba(0,0,0,0.05)] border border-border/50 bg-card"
      >
        <LetterGlitch
          glitchSpeed={50}
          centerVignette={true}
          outerVignette={false}
          smooth={true}
          glitchColors={['#2b4539', '#61dca3', '#61b3dc']}
        />
        
        {/* Minimalist Overlay Label */}
        <div className="absolute bottom-10 left-10 z-10">
          <h1 className="text-xl font-medium tracking-tight text-foreground uppercase">
            Letter Glitch
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Minimalist Atmospheric Loop
          </p>
        </div>

        {/* Minimalist Controls */}
        <div className="absolute top-10 right-10 z-10 flex gap-4">
          <button
            onClick={() => setRefreshKey(prev => prev + 1)}
            className="flex items-center gap-2 px-4 py-2 bg-background/80 backdrop-blur-md border border-border rounded-full text-xs font-medium hover:bg-accent hover:text-accent-foreground transition-all duration-300 shadow-sm"
          >
            <RotateCcw className="w-3 h-3" />
            REPLY
          </button>
        </div>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "letter-glitch-background",
  "description": "Minimalist canvas letter glitch background",
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.454.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4"
  }
}
~~~

~~~/src/Component.tsx
/**
 * LetterGlitchBackground Component
 * A high-end, minimalist canvas-based background effect that renders a grid of glitching characters.
 * Supports smooth color transitions, custom color palettes, and vignette effects.
 */

import React, { useRef, useEffect } from 'react';

export interface LetterGlitchProps {
  /** Array of hex colors for the glitching letters */
  glitchColors?: string[];
  /** Interval in milliseconds between glitch updates */
  glitchSpeed?: number;
  /** Whether to show a dark vignette from the center outwards */
  centerVignette?: boolean;
  /** Whether to show a dark vignette from the edges inwards */
  outerVignette?: boolean;
  /** Enable smooth color interpolation for transitions */
  smooth?: boolean;
  /** The set of characters to choose from for the glitch effect */
  characters?: string;
  /** CSS class name for the wrapper */
  className?: string;
}

export const LetterGlitch: React.FC<LetterGlitchProps> = ({
  glitchColors = ['#2b4539', '#61dca3', '#61b3dc'],
  glitchSpeed = 50,
  centerVignette = false,
  outerVignette = true,
  smooth = true,
  characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$&*()-_+=/[]{};:<>.,0123456789'
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number | null>(null);
  const letters = useRef<
    {
      char: string;
      color: string;
      targetColor: string;
      colorProgress: number;
    }[]
  >([]);
  const grid = useRef({ columns: 0, rows: 0 });
  const context = useRef<CanvasRenderingContext2D | null>(null);
  const lastGlitchTime = useRef(Date.now());
  const lettersAndSymbols = Array.from(characters);
  
  const fontSize = 16;
  const charWidth = 10;
  const charHeight = 20;

  const getRandomChar = () => {
    return lettersAndSymbols[Math.floor(Math.random() * lettersAndSymbols.length)];
  };

  const getRandomColor = () => {
    return glitchColors[Math.floor(Math.random() * glitchColors.length)];
  };

  const hexToRgb = (hex: string) => {
    const shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, (_m, r, g, b) => {
      return r + r + g + g + b + b;
    });
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
      ? {
          r: parseInt(result[1], 16),
          g: parseInt(result[2], 16),
          b: parseInt(result[3], 16)
        }
      : null;
  };

  const interpolateColor = (
    start: { r: number; g: number; b: number },
    end: { r: number; g: number; b: number },
    factor: number
  ) => {
    const result = {
      r: Math.round(start.r + (end.r - start.r) * factor),
      g: Math.round(start.g + (end.g - start.g) * factor),
      b: Math.round(start.b + (end.b - start.b) * factor)
    };
    return `rgb(${result.r}, ${result.g}, ${result.b})`;
  };

  const calculateGrid = (width: number, height: number) => {
    const columns = Math.ceil(width / charWidth);
    const rows = Math.ceil(height / charHeight);
    return { columns, rows };
  };

  const initializeLetters = (columns: number, rows: number) => {
    grid.current = { columns, rows };
    const totalLetters = columns * rows;
    letters.current = Array.from({ length: totalLetters }, () => ({
      char: getRandomChar(),
      color: getRandomColor(),
      targetColor: getRandomColor(),
      colorProgress: 1
    }));
  };

  const resizeCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const parent = canvas.parentElement;
    if (!parent) return;

    const dpr = window.devicePixelRatio || 1;
    const rect = parent.getBoundingClientRect();
    
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = `${rect.width}px`;
    canvas.style.height = `${rect.height}px`;

    if (context.current) {
      context.current.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    const { columns, rows } = calculateGrid(rect.width, rect.height);
    initializeLetters(columns, rows);
    drawLetters();
  };

  const drawLetters = () => {
    if (!context.current || !canvasRef.current || letters.current.length === 0) return;
    const ctx = context.current;
    const rect = canvasRef.current.getBoundingClientRect();
    
    ctx.clearRect(0, 0, rect.width, rect.height);
    ctx.font = `${fontSize}px monospace`;
    ctx.textBaseline = 'top';

    letters.current.forEach((letter, index) => {
      const x = (index % grid.current.columns) * charWidth;
      const y = Math.floor(index / grid.current.columns) * charHeight;
      ctx.fillStyle = letter.color;
      ctx.fillText(letter.char, x, y);
    });
  };

  const updateLetters = () => {
    if (!letters.current || letters.current.length === 0) return;
    const updateCount = Math.max(1, Math.floor(letters.current.length * 0.05));
    
    for (let i = 0; i < updateCount; i++) {
      const index = Math.floor(Math.random() * letters.current.length);
      if (!letters.current[index]) continue;
      
      letters.current[index].char = getRandomChar();
      letters.current[index].targetColor = getRandomColor();
      
      if (!smooth) {
        letters.current[index].color = letters.current[index].targetColor;
        letters.current[index].colorProgress = 1;
      } else {
        letters.current[index].colorProgress = 0;
      }
    }
  };

  const handleSmoothTransitions = () => {
    let needsRedraw = false;
    letters.current.forEach(letter => {
      if (letter.colorProgress < 1) {
        letter.colorProgress += 0.05;
        if (letter.colorProgress > 1) letter.colorProgress = 1;
        
        const startRgb = hexToRgb(letter.color.startsWith('rgb') ? '#000000' : letter.color); // Simplified fallback
        // Note: For a robust implementation, we'd store the actual start color hex
        const endRgb = hexToRgb(letter.targetColor);
        
        if (endRgb) {
          // If we're already in rgb format, we need to extract current r,g,b for precise interpolation
          // but for this effect, interpolating towards target is usually sufficient
          const currentRgb = letter.color.startsWith('rgb') 
            ? {
                r: parseInt(letter.color.match(/\d+/g)![0]),
                g: parseInt(letter.color.match(/\d+/g)![1]),
                b: parseInt(letter.color.match(/\d+/g)![2])
              }
            : hexToRgb(letter.color) || { r: 0, g: 0, b: 0 };

          letter.color = interpolateColor(currentRgb, endRgb, 0.1); // Constant step for smoothness
          needsRedraw = true;
        }
      }
    });
    
    if (needsRedraw) {
      drawLetters();
    }
  };

  const animate = () => {
    const now = Date.now();
    if (now - lastGlitchTime.current >= glitchSpeed) {
      updateLetters();
      drawLetters();
      lastGlitchTime.current = now;
    }

    if (smooth) {
      handleSmoothTransitions();
    }
    
    animationRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    context.current = canvas.getContext('2d');
    resizeCanvas();
    animate();

    let resizeTimeout: ReturnType<typeof setTimeout>;
    const handleResize = () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        if (animationRef.current) cancelAnimationFrame(animationRef.current);
        resizeCanvas();
        animate();
      }, 100);
    };

    window.addEventListener('resize', handleResize);
    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      window.removeEventListener('resize', handleResize);
    };
  }, [glitchSpeed, smooth, glitchColors, characters]);

  return (
    <div className="relative w-full h-full bg-background overflow-hidden">
      <canvas ref={canvasRef} className="block w-full h-full" />
      {outerVignette && (
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle,_transparent_60%,_hsl(var(--background))_100%)]" />
      )}
      {centerVignette && (
        <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle,_hsl(var(--background)/0.8)_0%,_transparent_60%)]" />
      )}
    </div>
  );
};

export default LetterGlitch;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
