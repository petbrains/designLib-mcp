You are given a task to integrate an existing React component in the codebase

~~~/README.md
# Magnet Lines

A grid of lines that rotate to point towards the cursor position, creating a magnetic field effect.

## Usage

```tsx
import MagnetLines from '@/sd-components/679ce99e-18b4-4c5f-a421-c1a3fd1bac4c';

function MyComponent() {
  return (
    <MagnetLines
      rows={9}
      columns={9}
      containerSize="60vmin"
      lineColor="tomato"
      lineWidth="0.8vmin"
      lineHeight="5vmin"
      baseAngle={0}
      style={{ margin: "2rem auto" }}
    />
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `rows` | `number` | `9` | Number of rows in the grid |
| `columns` | `number` | `9` | Number of columns in the grid |
| `containerSize` | `string` | `'80vmin'` | Width and height of the container |
| `lineColor` | `string` | `'#efefef'` | Color of the lines |
| `lineWidth` | `string` | `'1vmin'` | Width of each line |
| `lineHeight` | `string` | `'6vmin'` | Height of each line |
| `baseAngle` | `number` | `-10` | Initial rotation angle in degrees |
| `className` | `string` | `''` | Additional CSS classes |
| `style` | `CSSProperties` | `{}` | Inline styles |
~~~

~~~/src/App.tsx
import React from 'react';
import MagnetLines from './MagnetLines';

export default function App() {
  return (
    <div className="min-h-screen bg-[#1A1A1B] flex items-center justify-center p-8">
      <div className="relative w-full max-w-2xl aspect-square flex flex-col items-center justify-center p-8 rounded-2xl bg-[#222224] shadow-[0_0_40px_rgba(0,0,0,0.3)] overflow-hidden">
        
        <div className="absolute top-8 left-8 z-10">
          <h1 className="text-white text-2xl font-medium tracking-tight font-sans">Magnet Lines</h1>
          <p className="text-gray-400 text-sm mt-2">Interactive field animation</p>
        </div>

        <MagnetLines
          rows={12}
          columns={12}
          containerSize="70vmin"
          lineColor="rgba(255, 255, 255, 0.3)"
          lineWidth="2px"
          lineHeight="40px"
          baseAngle={0}
          style={{ margin: "0 auto" }}
        />
        
        <div className="absolute bottom-8 right-8 text-xs text-gray-500 font-mono">
          MOVE CURSOR
        </div>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "magnet-lines",
  "description": "A grid of lines that rotate to point towards the cursor position",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "framer-motion": "^10.0.0",
    "lucide-react": "^0.200.0"
  }
}
~~~

~~~/src/MagnetLines.tsx
import React, { useRef, useEffect, CSSProperties } from 'react';

export interface MagnetLinesProps {
  rows?: number;
  columns?: number;
  containerSize?: string;
  lineColor?: string;
  lineWidth?: string;
  lineHeight?: string;
  baseAngle?: number;
  className?: string;
  style?: CSSProperties;
}

const MagnetLines: React.FC<MagnetLinesProps> = ({
  rows = 9,
  columns = 9,
  containerSize = '80vmin',
  lineColor = '#efefef',
  lineWidth = '1vmin',
  lineHeight = '6vmin',
  baseAngle = -10,
  className = '',
  style = {}
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const items = container.querySelectorAll<HTMLSpanElement>('span');

    const onPointerMove = (pointer: { x: number; y: number }) => {
      items.forEach(item => {
        const rect = item.getBoundingClientRect();
        const centerX = rect.x + rect.width / 2;
        const centerY = rect.y + rect.height / 2;
        
        const b = pointer.x - centerX;
        const a = pointer.y - centerY;
        const c = Math.sqrt(a * a + b * b) || 1;
        const r = ((Math.acos(b / c) * 180) / Math.PI) * (pointer.y > centerY ? 1 : -1);
        
        item.style.setProperty('--rotate', `${r}deg`);
      });
    };

    const handlePointerMove = (e: PointerEvent) => {
      onPointerMove({ x: e.x, y: e.y });
    };

    window.addEventListener('pointermove', handlePointerMove);
    
    // Trigger initial calculation
    if (items.length) {
      const middleIndex = Math.floor(items.length / 2);
      const rect = items[middleIndex].getBoundingClientRect();
      onPointerMove({ x: rect.x, y: rect.y });
    }

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
    };
  }, []);

  const total = rows * columns;
  
  // Create spans with inline styles for the base rotation
  const spans = Array.from({ length: total }, (_, i) => (
    <span
      key={i}
      className="block origin-center"
      style={{
        backgroundColor: lineColor,
        width: lineWidth,
        height: lineHeight,
        // @ts-ignore
        '--rotate': `${baseAngle}deg`,
        transform: 'rotate(var(--rotate))',
        willChange: 'transform'
      }}
    />
  ));

  return (
    <div
      ref={containerRef}
      className={`grid place-items-center ${className}`}
      style={{
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gridTemplateRows: `repeat(${rows}, 1fr)`,
        width: containerSize,
        height: containerSize,
        ...style
      }}
    >
      {spans}
    </div>
  );
};

export default MagnetLines;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
