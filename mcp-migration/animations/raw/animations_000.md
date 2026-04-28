You are given a task to integrate an existing React component in the codebase

~~~/README.md
# ForceFieldBackground

A high-performance, interactive particle system background that reacts to mouse movement with a magnetic "force field" effect. Built with p5.js and React.

## Features

- **Interactive Force Field**: Particles disperse as the mouse moves through them.
- **Image-Based Mapping**: Particles are generated based on the brightness map of an underlying image (defaults to a mountain landscape).
- **Dynamic Physics**: Fluid motion with friction and restoration forces.
- **Customizable**: Control hue, saturation, particle density, stroke width, and force field physics.
- **Production Ready**: Responsive canvas resizing, proper React cleanup, and TypeScript support.

## Dependencies

- `p5`: For high-performance canvas rendering
- `react`: Core framework

## Usage

```tsx
import { ForceFieldBackground } from '@/sd-components/febbd3b8-b30b-407b-a997-55442e42be27';

function MyPage() {
  return (
    <div className="relative w-screen h-screen">
      <ForceFieldBackground 
        hue={210} 
        spacing={10} 
        forceStrength={15}
      />
      
      <div className="absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
        <h1 className="text-white text-6xl font-bold mix-blend-overlay">
          Hello World
        </h1>
      </div>
    </div>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `imageUrl` | string | (Mountain Image) | Source image URL for particle mapping |
| `hue` | number | 210 | Base color hue (0-360) |
| `saturation` | number | 100 | Color saturation (0-100) |
| `spacing` | number | 10 | Grid spacing (lower = more particles) |
| `density` | number | 2.0 | Random density factor |
| `minStroke` | number | 2 | Minimum particle size |
| `maxStroke` | number | 6 | Maximum particle size |
| `forceStrength` | number | 10 | Strength of cursor repulsion |
| `magnifierRadius` | number | 150 | Radius of interaction area |
| `friction` | number | 0.9 | Movement friction (0.5-0.99) |
| `restoreSpeed` | number | 0.05 | Speed of return to origin |

## Notes

- The component automatically fills its parent container. Ensure the parent has dimensions.
- Mouse interaction is relative to the canvas.
- For best performance, avoid setting `spacing` lower than 5 on large screens.
~~~

~~~/src/App.tsx
import React, { useState } from 'react';
import { ForceFieldBackground } from './Component';
import { RefreshCw, Zap, Sliders, Maximize, Palette } from 'lucide-react';

export default function App() {
  const [params, setParams] = useState({
    hue: 210,
    saturation: 100,
    minStroke: 2,
    maxStroke: 6,
    spacing: 10,
    forceStrength: 10,
    magnifierRadius: 150
  });

  const randomize = () => {
    setParams({
      ...params,
      hue: Math.floor(Math.random() * 360),
      minStroke: parseFloat((Math.random() * 3 + 1).toFixed(1)),
      maxStroke: parseFloat((Math.random() * 8 + 4).toFixed(1)),
      spacing: Math.floor(Math.random() * 8 + 8),
      magnifierRadius: Math.floor(Math.random() * 100 + 100)
    });
  };

  return (
    <div className="relative w-full min-h-screen font-sans text-white bg-black overflow-hidden">
      {/* Background Component */}
      <div className="absolute inset-0 z-0">
        <ForceFieldBackground 
          hue={params.hue}
          saturation={params.saturation}
          minStroke={params.minStroke}
          maxStroke={params.maxStroke}
          spacing={params.spacing}
          forceStrength={params.forceStrength}
          magnifierRadius={params.magnifierRadius}
        />
      </div>

      {/* Foreground Content Overlay */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen pointer-events-none">
        <div className="text-center space-y-8 p-8 max-w-4xl mix-blend-difference">
          <h1 className="text-7xl md:text-9xl font-bold tracking-tighter leading-none bg-clip-text text-transparent bg-gradient-to-b from-white to-white/50"
              style={{ fontFamily: '"Inter", sans-serif' }}>
            FORCE FIELD
          </h1>
          <p className="text-xl md:text-2xl font-light tracking-[0.5em] text-white/80 uppercase">
            Interactive Particle System
          </p>
        </div>
      </div>

      {/* Floating Controls (Pointer events enabled) */}
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-20 flex gap-4 pointer-events-auto">
        <div className="bg-black/40 backdrop-blur-md border border-white/10 p-4 rounded-2xl shadow-2xl flex items-center gap-6 animate-in slide-in-from-bottom-10 fade-in duration-700">
          
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2 text-xs text-white/50 uppercase tracking-wider">
              <Palette className="w-3 h-3" /> Hue
            </div>
            <input 
              type="range" min="0" max="360" 
              value={params.hue} 
              onChange={(e) => setParams({...params, hue: parseInt(e.target.value)})}
              className="w-24 accent-white h-1 bg-white/20 rounded-full appearance-none cursor-pointer"
            />
          </div>

          <div className="w-px h-8 bg-white/10" />

          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2 text-xs text-white/50 uppercase tracking-wider">
              <Maximize className="w-3 h-3" /> Radius
            </div>
            <input 
              type="range" min="50" max="300" 
              value={params.magnifierRadius} 
              onChange={(e) => setParams({...params, magnifierRadius: parseInt(e.target.value)})}
              className="w-24 accent-white h-1 bg-white/20 rounded-full appearance-none cursor-pointer"
            />
          </div>

          <div className="w-px h-8 bg-white/10" />

          <div className="flex flex-col gap-2">
             <div className="flex items-center gap-2 text-xs text-white/50 uppercase tracking-wider">
              <Zap className="w-3 h-3" /> Force
            </div>
            <input 
              type="range" min="0" max="30" 
              value={params.forceStrength} 
              onChange={(e) => setParams({...params, forceStrength: parseInt(e.target.value)})}
              className="w-24 accent-white h-1 bg-white/20 rounded-full appearance-none cursor-pointer"
            />
          </div>

          <button 
            onClick={randomize}
            className="ml-4 p-3 rounded-full bg-white/10 hover:bg-white/20 transition-colors border border-white/10 group"
            title="Randomize Parameters"
          >
            <RefreshCw className="w-5 h-5 text-white/80 group-hover:rotate-180 transition-transform duration-500" />
          </button>
        </div>
      </div>

      <div className="fixed top-8 right-8 z-20 pointer-events-none">
        <div className="bg-black/20 backdrop-blur-sm border border-white/5 px-4 py-2 rounded-full text-xs text-white/30 font-mono">
          FPS: 60 • POINTS: {(1280/params.spacing * 720/params.spacing * 0.5).toFixed(0)}
        </div>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "force-field-background",
  "description": "Interactive p5.js force field background component",
  "dependencies": {
    "p5": "^1.9.0",
    "lucide-react": "^0.344.0"
  }
}
~~~

~~~/src/Component.tsx
import React, { useEffect, useRef, useState } from 'react';
import p5 from 'p5';

export interface ForceFieldBackgroundProps {
  /**
   * URL of the image to use as the base for the particle field
   * @default "https://cdn.pixabay.com/photo/2024/12/13/20/29/alps-9266131_1280.jpg"
   */
  imageUrl?: string;
  /**
   * Base hue for the color palette (0-360)
   * @default 210
   */
  hue?: number;
  /**
   * Color saturation (0-100)
   * @default 100
   */
  saturation?: number;
  /**
   * Brightness threshold for particle visibility (0-255)
   * @default 255
   */
  threshold?: number;
  /**
   * Minimum stroke weight for particles
   * @default 2
   */
  minStroke?: number;
  /**
   * Maximum stroke weight for particles
   * @default 6
   */
  maxStroke?: number;
  /**
   * Spacing between particles (lower = more density)
   * @default 10
   */
  spacing?: number;
  /**
   * Noise scale for particle placement irregularity
   * @default 0
   */
  noiseScale?: number;
  /**
   * Density factor (probability of particle existence)
   * @default 2.0
   */
  density?: number;
  /**
   * Invert the source image brightness mapping
   * @default true
   */
  invertImage?: boolean;
  /**
   * Invert the wireframe/particle visibility condition
   * @default true
   */
  invertWireframe?: boolean;
  /**
   * Enable the magnifier/force field effect
   * @default true
   */
  magnifierEnabled?: boolean;
  /**
   * Radius of the force field effect around the cursor
   * @default 150
   */
  magnifierRadius?: number;
  /**
   * Strength of the force pushing particles away
   * @default 10
   */
  forceStrength?: number;
  /**
   * Friction factor for particle movement (0-1)
   * @default 0.9
   */
  friction?: number;
  /**
   * Speed at which particles return to original position
   * @default 0.05
   */
  restoreSpeed?: number;
  /**
   * Additional CSS class names
   */
  className?: string;
}

/**
 * ForceFieldBackground
 * 
 * An interactive, particle-based background that reacts to mouse movement.
 * It uses an underlying image to determine particle color and size, creating
 * a "force field" effect where particles are pushed away by the cursor.
 */
export function ForceFieldBackground({
  imageUrl = "https://cdn.pixabay.com/photo/2024/12/13/20/29/alps-9266131_1280.jpg",
  hue = 210,
  saturation = 100,
  threshold = 255,
  minStroke = 2,
  maxStroke = 6,
  spacing = 10,
  noiseScale = 0,
  density = 2.0,
  invertImage = true,
  invertWireframe = true,
  magnifierEnabled = true,
  magnifierRadius = 150,
  forceStrength = 10,
  friction = 0.9,
  restoreSpeed = 0.05,
  className = "",
}: ForceFieldBackgroundProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const p5InstanceRef = useRef<p5 | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Keep latest props in ref to access inside p5 closure without re-instantiating
  const propsRef = useRef({
    hue, saturation, threshold, minStroke, maxStroke, spacing, noiseScale, 
    density, invertImage, invertWireframe, magnifierEnabled, magnifierRadius,
    forceStrength, friction, restoreSpeed
  });

  useEffect(() => {
    propsRef.current = {
      hue, saturation, threshold, minStroke, maxStroke, spacing, noiseScale,
      density, invertImage, invertWireframe, magnifierEnabled, magnifierRadius,
      forceStrength, friction, restoreSpeed
    };
  }, [hue, saturation, threshold, minStroke, maxStroke, spacing, noiseScale, density, invertImage, invertWireframe, magnifierEnabled, magnifierRadius, forceStrength, friction, restoreSpeed]);

  useEffect(() => {
    if (!containerRef.current) return;

    // Cleanup previous instance if exists
    if (p5InstanceRef.current) {
      p5InstanceRef.current.remove();
    }

    const sketch = (p: p5) => {
      let originalImg: p5.Image;
      let img: p5.Image;
      let palette: p5.Color[] = [];
      let points: {
        pos: p5.Vector;
        originalPos: p5.Vector;
        vel: p5.Vector;
      }[] = [];
      
      // Internal state tracking to detect changes
      let lastHue = -1;
      let lastSaturation = -1;
      let lastSpacing = -1;
      let lastNoiseScale = -1;
      let lastDensity = -1;
      let lastInvertImage: boolean | null = null;
      let magnifierX = 0;
      let magnifierY = 0;
      let magnifierInertia = 0.1;

      p.preload = () => {
        // Use p5's loadImage with callbacks
        p.loadImage(
          imageUrl,
          (loadedImg) => {
            originalImg = loadedImg;
            setIsLoading(false);
          },
          (err) => {
            console.error("Failed to load image", err);
            setError("Failed to load image");
            setIsLoading(false);
          }
        );
      };

      p.setup = () => {
        if (!originalImg) return; // Should be loaded by preload
        
        // Create canvas to fill parent
        const { clientWidth, clientHeight } = containerRef.current!;
        p.createCanvas(clientWidth, clientHeight);
        
        // Initialize magnifier position
        magnifierX = p.width / 2;
        magnifierY = p.height / 2;

        processImage();
        generatePalette(propsRef.current.hue, propsRef.current.saturation);
        generatePoints();
      };

      p.windowResized = () => {
        if (!containerRef.current || !originalImg) return;
        const { clientWidth, clientHeight } = containerRef.current;
        p.resizeCanvas(clientWidth, clientHeight);
        processImage();
        generatePoints();
      };

      function processImage() {
        if (!originalImg) return;
        img = originalImg.get();
        // Resize image to match canvas for 1:1 pixel mapping
        if (p.width > 0 && p.height > 0) {
          img.resize(p.width, p.height);
        }
        img.filter(p.GRAY);

        if (propsRef.current.invertImage) {
          img.loadPixels();
          for (let i = 0; i < img.pixels.length; i += 4) {
            img.pixels[i] = 255 - img.pixels[i];
            img.pixels[i + 1] = 255 - img.pixels[i + 1];
            img.pixels[i + 2] = 255 - img.pixels[i + 2];
          }
          img.updatePixels();
        }
        lastInvertImage = propsRef.current.invertImage;
      }

      function generatePalette(h: number, s: number) {
        palette = [];
        p.push();
        p.colorMode(p.HSL);
        for (let i = 0; i < 12; i++) {
          let lightness = p.map(i, 0, 11, 95, 5);
          palette.push(p.color(h, s, lightness));
        }
        p.pop();
      }

      function generatePoints() {
        if (!img) return;
        points = [];
        const { spacing, density, noiseScale } = propsRef.current;
        
        // Guard against infinite loop or too many points
        const safeSpacing = Math.max(2, spacing); 

        for (let y = 0; y < img.height; y += safeSpacing) {
          for (let x = 0; x < img.width; x += safeSpacing) {
            if (p.random() > density) continue;
            
            let nx = p.noise(x * noiseScale, y * noiseScale) - 0.5;
            let ny = p.noise((x + 500) * noiseScale, (y + 500) * noiseScale) - 0.5;
            let px = x + nx * safeSpacing;
            let py = y + ny * safeSpacing;
            
            points.push({
              pos: p.createVector(px, py),
              originalPos: p.createVector(px, py),
              vel: p.createVector(0, 0)
            });
          }
        }
        
        lastSpacing = spacing;
        lastNoiseScale = noiseScale;
        lastDensity = density;
      }

      function applyForceField(mx: number, my: number) {
        const props = propsRef.current;
        if (!props.magnifierEnabled) return;

        for (let pt of points) {
          // Repel force
          let dir = p5.Vector.sub(pt.pos, p.createVector(mx, my));
          let d = dir.mag();
          
          if (d < props.magnifierRadius) {
            dir.normalize();
            let force = dir.mult(props.forceStrength / Math.max(1, d)); // Avoid div by zero
            pt.vel.add(force);
          }
          
          // Friction
          pt.vel.mult(props.friction);
          
          // Restore force (spring back to original)
          let restore = p5.Vector.sub(pt.pos, pt.originalPos).mult(-props.restoreSpeed);
          pt.vel.add(restore);
          
          // Update position
          pt.pos.add(pt.vel);
        }
      }

      p.draw = () => {
        if (!img) return;
        p.background(0);

        const props = propsRef.current;

        // Check for prop changes that require regeneration
        if (props.hue !== lastHue || props.saturation !== lastSaturation) {
          generatePalette(props.hue, props.saturation);
          lastHue = props.hue;
          lastSaturation = props.saturation;
        }

        if (props.invertImage !== lastInvertImage) {
          processImage(); // This sets lastInvertImage
        }

        if (props.spacing !== lastSpacing || props.noiseScale !== lastNoiseScale || props.density !== lastDensity) {
          generatePoints();
        }

        // Mouse interaction
        // Use lerp for smooth movement of the 'magnifier' center
        magnifierX = p.lerp(magnifierX, p.mouseX, magnifierInertia);
        magnifierY = p.lerp(magnifierY, p.mouseY, magnifierInertia);

        applyForceField(magnifierX, magnifierY);

        img.loadPixels();
        p.noFill();

        for (let pt of points) {
          let x = pt.pos.x;
          let y = pt.pos.y;
          let d = p.dist(x, y, magnifierX, magnifierY);
          
          let px = p.constrain(p.floor(x), 0, img.width - 1);
          let py = p.constrain(p.floor(y), 0, img.height - 1);
          
          // Access pixel data (RGBA)
          let index = (px + py * img.width) * 4;
          // Just use R channel since it's grayscale
          let brightness = img.pixels[index]; 
          
          // Guard against undefined brightness if image resized or not ready
          if (brightness === undefined) continue;

          let condition = props.invertWireframe
            ? brightness < props.threshold
            : brightness > props.threshold;

          if (condition) {
            let shadeIndex = Math.floor(p.map(brightness, 0, 255, 0, palette.length - 1));
            shadeIndex = p.constrain(shadeIndex, 0, palette.length - 1);
            
            let strokeSize = p.map(brightness, 0, 255, props.minStroke, props.maxStroke);
            
            if (props.magnifierEnabled && d < props.magnifierRadius) {
              let factor = p.map(d, 0, props.magnifierRadius, 2, 1); // 2x size at center
              strokeSize *= factor;
            }
            
            if (palette[shadeIndex]) {
              p.stroke(palette[shadeIndex]);
              p.strokeWeight(strokeSize);
              p.point(x, y);
            }
          }
        }
      };
    };

    const myP5 = new p5(sketch, containerRef.current);
    p5InstanceRef.current = myP5;

    return () => {
      myP5.remove();
    };
  }, [imageUrl]); // Re-init if imageUrl changes

  return (
    <div 
      className={`relative w-full h-full overflow-hidden bg-black ${className}`} 
      ref={containerRef}
    >
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center text-white/50 text-xs tracking-widest uppercase">
          Initializing Force Field...
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center text-red-500/50 text-xs tracking-widest uppercase">
          {error}
        </div>
      )}
    </div>
  );
}

export default ForceFieldBackground;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design

Here is a reference implementation of a Gooey Gradient Background

~~~/README.md
# Gooey Gradient Background

A mesmerizing, interactive gooey liquid gradient background with animated blobs and mouse-following effect. This component creates an immersive visual experience using SVG filters and CSS animations.

## Features

- 🎨 **Liquid "Gooey" Effect**: Uses SVG `feColorMatrix` and `feGaussianBlur` filters to create merging blob effects.
- 🖱️ **Interactive**: Includes a mouse-following gradient blob that interacts with the background.
- 🌈 **Vibrant Gradients**: Complex, multi-layered gradient animations.
- 🚀 **Performance Optimized**: Uses CSS transforms and `requestAnimationFrame` for smooth rendering.
- 📱 **Responsive**: Adapts to container size.

## Usage

```tsx
import { GooeyGradientBackground } from '@/sd-components/942b8e8e-129e-4697-b695-3b1397a42949';

export default function HeroSection() {
  return (
    <div className="h-screen w-full">
      <GooeyGradientBackground>
        <div className="flex items-center justify-center h-full">
          <h1 className="text-white text-6xl font-bold">Welcome</h1>
        </div>
      </GooeyGradientBackground>
    </div>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | `undefined` | Content to render on top of the background |
| `className` | `string` | `''` | Additional classes for the container |

## Implementation Details

The component uses a combination of:
1. **CSS Keyframes**: For independent movement of 5 distinct gradient blobs.
2. **SVG Filters**: A hidden SVG provides the `#goo` filter reference used by the container.
3. **React Ref & JS**: Handles the mouse interaction logic to update the `transform` of the interactive blob without triggering React re-renders.
~~~

~~~/src/App.tsx
import React from 'react';
import { GooeyGradientBackground } from './Component';

export default function App() {
  return (
    <div className="w-full h-screen">
      <GooeyGradientBackground>
        <div className="flex flex-col items-center justify-center w-full h-full text-white/90">
          <h1 className="text-[96px] leading-none font-light select-none tracking-wide drop-shadow-sm" style={{ fontFamily: 'Dongle, sans-serif' }}>
            Bubbles
          </h1>
          <p className="text-2xl mt-4 font-light opacity-80 max-w-md text-center px-4" style={{ fontFamily: 'Dongle, sans-serif' }}>
            Move your mouse to interact with the gradient field.
          </p>
          
          <div className="mt-12 flex gap-4">
             <button className="px-8 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-xl hover:bg-white/20 transition-all cursor-pointer" style={{ fontFamily: 'Dongle, sans-serif' }}>
                Get Started
             </button>
             <button className="px-8 py-3 bg-transparent border border-white/20 rounded-full text-xl hover:bg-white/5 transition-all cursor-pointer" style={{ fontFamily: 'Dongle, sans-serif' }}>
                Learn More
             </button>
          </div>
        </div>
      </GooeyGradientBackground>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "gooey-gradient-background",
  "description": "A mesmerizing, interactive gooey liquid gradient background with animated blobs",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0"
  }
}
~~~

~~~/src/Component.css
.gooey-wrapper {
  /* Using the specific colors from the design */
  --color-bg1: rgb(108, 0, 162);
  --color-bg2: rgb(0, 17, 82);
  --color1: 18, 113, 255;
  --color2: 221, 74, 255;
  --color3: 100, 220, 255;
  --color4: 200, 50, 50;
  --color5: 180, 180, 50;
  --color-interactive: 140, 100, 255;
  --circle-size: 80%;
  --blending: hard-light;
  
  font-family: 'Dongle', sans-serif;
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

@keyframes moveInCircle {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
  100% { transform: rotate(360deg); }
}

@keyframes moveVertical {
  0% { transform: translateY(-50%); }
  50% { transform: translateY(50%); }
  100% { transform: translateY(-50%); }
}

@keyframes moveHorizontal {
  0% { transform: translateX(-50%) translateY(-10%); }
  50% { transform: translateX(50%) translateY(10%); }
  100% { transform: translateX(-50%) translateY(-10%); }
}

.gradient-bg {
  width: 100%;
  height: 100%;
  position: absolute;
  overflow: hidden;
  background: linear-gradient(40deg, var(--color-bg1), var(--color-bg2));
  top: 0;
  left: 0;
  z-index: 0;
}

.gradient-bg svg {
  position: fixed;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
}

.gradients-container {
  filter: url(#goo) blur(40px);
  width: 100%;
  height: 100%;
}

.g1 {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color1), 0.8) 0, rgba(var(--color1), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);
  transform-origin: center center;
  animation: moveVertical 30s ease infinite;
  opacity: 1;
}

.g2 {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color2), 0.8) 0, rgba(var(--color2), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);
  transform-origin: calc(50% - 400px);
  animation: moveInCircle 20s reverse infinite;
  opacity: 1;
}

.g3 {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color3), 0.8) 0, rgba(var(--color3), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2 + 200px);
  left: calc(50% - var(--circle-size) / 2 - 500px);
  transform-origin: calc(50% + 400px);
  animation: moveInCircle 40s linear infinite;
  opacity: 1;
}

.g4 {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color4), 0.8) 0, rgba(var(--color4), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: var(--circle-size);
  height: var(--circle-size);
  top: calc(50% - var(--circle-size) / 2);
  left: calc(50% - var(--circle-size) / 2);
  transform-origin: calc(50% - 200px);
  animation: moveHorizontal 40s ease infinite;
  opacity: 0.7;
}

.g5 {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color5), 0.8) 0, rgba(var(--color5), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: calc(var(--circle-size) * 2);
  height: calc(var(--circle-size) * 2);
  top: calc(50% - var(--circle-size));
  left: calc(50% - var(--circle-size));
  transform-origin: calc(50% - 800px) calc(50% + 200px);
  animation: moveInCircle 20s ease infinite;
  opacity: 1;
}

.interactive {
  position: absolute;
  background: radial-gradient(circle at center, rgba(var(--color-interactive), 0.8) 0, rgba(var(--color-interactive), 0) 50%) no-repeat;
  mix-blend-mode: var(--blending);
  width: 100%;
  height: 100%;
  top: -50%;
  left: -50%;
  opacity: 0.7;
  /* Will be controlled by JS for performance */
}
~~~

~~~/src/Component.tsx
import React, { useEffect, useRef } from 'react';
import './Component.css';

interface GooeyGradientBackgroundProps {
  /**
   * Content to render on top of the background
   */
  children?: React.ReactNode;
  /**
   * Additional class names for the container
   */
  className?: string;
}

/**
 * A mesmerizing, interactive gooey liquid gradient background with animated blobs.
 * Features:
 * - Pure CSS animations for background blobs
 * - SVG filter for the "gooey" liquid effect
 * - Interactive mouse-following blob
 * - Responsive and container-aware
 */
export function GooeyGradientBackground({ children, className = '' }: GooeyGradientBackgroundProps) {
  const interactiveRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let curX = 0;
    let curY = 0;
    let tgX = 0;
    let tgY = 0;

    const handleMouseMove = (event: MouseEvent) => {
      tgX = event.clientX;
      tgY = event.clientY;
    };

    const animate = () => {
      if (!interactiveRef.current) return;
      
      curX += (tgX - curX) / 20;
      curY += (tgY - curY) / 20;
      
      interactiveRef.current.style.transform = `translate(${Math.round(curX)}px, ${Math.round(curY)}px)`;
      requestAnimationFrame(animate);
    };

    window.addEventListener('mousemove', handleMouseMove);
    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className={`gooey-wrapper w-full h-full relative overflow-hidden ${className}`}>
      <div className="gradient-bg">
        <svg xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="goo">
              <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
              <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
              <feBlend in="SourceGraphic" in2="goo" />
            </filter>
          </defs>
        </svg>
        <div className="gradients-container">
          <div className="g1"></div>
          <div className="g2"></div>
          <div className="g3"></div>
          <div className="g4"></div>
          <div className="g5"></div>
          <div ref={interactiveRef} className="interactive"></div>
        </div>
      </div>
      
      {/* Content Layer */}
      <div className="relative z-10 w-full h-full">
        {children}
      </div>
    </div>
  );
}

export default GooeyGradientBackground;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design

This is a reference implementation of an interactive 3D background

~~~/README.md
# Tubes Interactive Background

A high-performance 3D interactive background featuring neon tubes that follow the user's cursor. Built with `threejs-components`.

## Features
- 🖱️ **Interactive Cursor**: Tubes follow mouse movement in 3D space
- 🎨 **Dynamic Colors**: Click to randomize tube and light colors instantly
- ⚡ **High Performance**: Optimized WebGL rendering
- 📱 **Responsive**: Adapts to container size

## Dependencies
- `three`
- `framer-motion` (optional, for overlay animations)

## Usage

```tsx
import { TubesBackground } from '@/sd-components/070b9477-5ebf-41b4-ab04-9b4d4975e984';

function MyPage() {
  return (
    <div style={{ height: '100vh' }}>
      <TubesBackground>
        {/* Your content overlay goes here */}
        <h1>Hello World</h1>
      </TubesBackground>
    </div>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | `undefined` | Content to overlay on top of the canvas |
| `className` | `string` | `undefined` | Additional CSS classes for the container |
| `enableClickInteraction` | `boolean` | `true` | Whether clicking randomizes colors |

## Credits
Original concept and implementation by [Kevin Levron](https://www.framer.com/@kevin-levron/).
Based on `threejs-components` library.
~~~

~~~/src/App.tsx
import React from 'react';
import { TubesBackground } from './Component';
import { ExternalLink, MousePointer2 } from 'lucide-react';

export default function App() {
  return (
    <div className="w-full h-screen font-sans">
      <TubesBackground>
        <div className="flex flex-col items-center justify-center w-full h-full gap-6 text-center px-4">
          <div className="space-y-2 pointer-events-auto cursor-default">
            <h1 className="text-6xl md:text-8xl font-bold uppercase tracking-tighter text-white drop-shadow-[0_0_20px_rgba(0,0,0,1)] select-none">
              Tubes
            </h1>
            <h2 className="text-4xl md:text-6xl font-medium uppercase tracking-tight text-white/90 drop-shadow-[0_0_20px_rgba(0,0,0,1)] select-none">
              Cursor
            </h2>
          </div>
          
          <div className="mt-8 flex flex-col items-center gap-4 pointer-events-auto">
            <p className="text-white/80 text-sm max-w-md drop-shadow-md">
              Move your cursor to interact with the 3D tubes. Click anywhere to randomize the neon colors.
            </p>
            
            <a 
              href="https://www.framer.com/@kevin-levron/" 
              target="_blank" 
              rel="noreferrer"
              className="flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 rounded-full text-white transition-all duration-300 group"
            >
              <span>Original Concept</span>
              <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </a>
          </div>

          <div className="absolute bottom-8 flex flex-col items-center gap-2 text-white/50 animate-pulse pointer-events-none">
            <MousePointer2 className="w-6 h-6" />
            <span className="text-xs uppercase tracking-widest">Click to randomize</span>
          </div>
        </div>
      </TubesBackground>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "tubes-interactive-background",
  "description": "Interactive neon tubes 3D cursor effect background",
  "dependencies": {
    "three": "^0.160.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.300.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0"
  }
}
~~~

~~~/src/Component.tsx
import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from './utils'; // We'll define this or use inline

// Helper for random colors
const randomColors = (count: number) => {
  return new Array(count)
    .fill(0)
    .map(() => "#" + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0'));
};

interface TubesBackgroundProps {
  children?: React.ReactNode;
  className?: string;
  enableClickInteraction?: boolean;
}

export function TubesBackground({ 
  children, 
  className,
  enableClickInteraction = true 
}: TubesBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const tubesRef = useRef<any>(null);

  useEffect(() => {
    let mounted = true;
    let cleanup: (() => void) | undefined;

    const initTubes = async () => {
      if (!canvasRef.current) return;

      try {
        // We use the specific build from the CDN as it contains the exact effect requested
        // Using native dynamic import which works in modern browsers
        // @ts-ignore
        const module = await import('https://cdn.jsdelivr.net/npm/threejs-components@0.0.19/build/cursors/tubes1.min.js');
        const TubesCursor = module.default;

        if (!mounted) return;

        const app = TubesCursor(canvasRef.current, {
          tubes: {
            colors: ["#f967fb", "#53bc28", "#6958d5"],
            lights: {
              intensity: 200,
              colors: ["#83f36e", "#fe8a2e", "#ff008a", "#60aed5"]
            }
          }
        });

        tubesRef.current = app;
        setIsLoaded(true);

        // Handle resize if the library doesn't automatically
        const handleResize = () => {
          // The library might handle it, but typically we ensure canvas matches container
          // For this specific lib, it likely attaches to window resize or we might need to manually resize
        };

        window.addEventListener('resize', handleResize);
        
        cleanup = () => {
          window.removeEventListener('resize', handleResize);
          // If the library has a destroy method, call it
          // app.destroy?.(); 
          // Based on typical threejs-components, it might not have an explicit destroy exposed easily
          // but we should at least nullify the ref
        };

      } catch (error) {
        console.error("Failed to load TubesCursor:", error);
      }
    };

    initTubes();

    return () => {
      mounted = false;
      if (cleanup) cleanup();
    };
  }, []);

  const handleClick = () => {
    if (!enableClickInteraction || !tubesRef.current) return;
    
    const colors = randomColors(3);
    const lightsColors = randomColors(4);
    
    tubesRef.current.tubes.setColors(colors);
    tubesRef.current.tubes.setLightsColors(lightsColors);
  };

  return (
    <div 
      className={cn("relative w-full h-full min-h-[400px] overflow-hidden bg-background", className)}
      onClick={handleClick}
    >
      <canvas 
        ref={canvasRef} 
        className="absolute inset-0 w-full h-full block"
        style={{ touchAction: 'none' }}
      />
      
      {/* Content Overlay */}
      <div className="relative z-10 w-full h-full pointer-events-none">
        {children}
      </div>
    </div>
  );
}

// Default export
export default TubesBackground;

// Utility for class merging
function cn(...inputs: (string | undefined | null | false)[]) {
  return inputs.filter(Boolean).join(" ");
}
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design

This is a reference implementation of a parallax stars background

~~~/README.md
# Parallax Stars Background

A mesmerizing space-themed background component with animated parallax pixel stars and a radial gradient atmosphere.

## Features
- **Pure CSS/JS Animation**: Uses efficient `box-shadow` rendering for thousands of particles.
- **Parallax Effect**: Three layers of stars moving at different speeds to create depth.
- **Radial Gradient Atmosphere**: Creates a deep space feel.
- **Customizable**: Adjustable speed and title text.
- **Responsive**: Adapts to screen size.

## Usage

```tsx
import { ParallaxStarsBackground } from '@/sd-components/a17695b3-944f-4e4b-9d72-b0cfd61b9bb8';

function App() {
  return (
    <ParallaxStarsBackground 
      title="MY AWESOME\nSPACE APP" 
      speed={1.5}
    >
      <button className="px-6 py-2 border border-white text-white hover:bg-white hover:text-black transition-colors rounded-full uppercase tracking-widest text-sm">
        Enter the Void
      </button>
    </ParallaxStarsBackground>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | "PURE CSS\nPARALLAX PIXEL STARS" | Main title text. Use `\n` for line breaks. |
| `children` | `ReactNode` | undefined | Optional content to render below the title. |
| `className` | `string` | "" | Additional classes for the container. |
| `speed` | `number` | 1 | Animation speed multiplier. Higher is faster. |
~~~

~~~/src/App.tsx
import React from 'react';
import { ParallaxStarsBackground } from './Component';

export default function App() {
  return (
    <div className="w-full min-h-screen">
      <ParallaxStarsBackground 
        speed={1}
      />
    </div>
  );
}
~~~

~~~/package.json

{
  "name": "parallax-stars-background",
  "version": "1.0.0",
  "description": "A mesmerizing space-themed background with animated parallax pixel stars and a radial gradient atmosphere.",
  "main": "src/Component.tsx",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0",
    "framer-motion": "^11.0.8",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  }
}
~~~

~~~/src/Component.tsx
import React, { useMemo } from 'react';

// Types for the component props
export interface ParallaxStarsBackgroundProps {
  /**
   * Title text to display in the center
   * @default "PURE CSS PARALLAX PIXEL STARS"
   */
  title?: string;
  /**
   * Subtitle or additional content
   */
  children?: React.ReactNode;
  /**
   * Class name for the container
   */
  className?: string;
  /**
   * Speed multiplier for the animation
   * @default 1
   */
  speed?: number;
}

// Helper to generate random box shadows
const generateBoxShadows = (n: number) => {
  let value = `${Math.floor(Math.random() * 2000)}px ${Math.floor(Math.random() * 2000)}px #FFF`;
  for (let i = 2; i <= n; i++) {
    value += `, ${Math.floor(Math.random() * 2000)}px ${Math.floor(Math.random() * 2000)}px #FFF`;
  }
  return value;
};

export function ParallaxStarsBackground({
  title = "PURE CSS\nPARALLAX PIXEL STARS",
  children,
  className = "",
  speed = 1
}: ParallaxStarsBackgroundProps) {
  // Memoize shadows so they don't regenerate on re-renders
  const shadowsSmall = useMemo(() => generateBoxShadows(700), []);
  const shadowsMedium = useMemo(() => generateBoxShadows(200), []);
  const shadowsBig = useMemo(() => generateBoxShadows(100), []);

  return (
    <div className={`relative w-full h-screen overflow-hidden bg-[#090A0F] font-['Lato'] ${className}`}>
      {/* Inline styles for the gradient and animations */}
      <style>{`
        .bg-radial-space {
          background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        }
        @keyframes animStar {
          from { transform: translateY(0px); }
          to { transform: translateY(-2000px); }
        }
        .text-gradient-clip {
          background: linear-gradient(to bottom, white 0%, #38495a 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
      `}</style>

      {/* Background Gradient */}
      <div className="absolute inset-0 bg-radial-space z-0" />

      {/* Stars Layer 1 (Small) */}
      <div 
        className="absolute left-0 top-0 w-[1px] h-[1px] bg-transparent z-10 animate-[animStar_50s_linear_infinite]"
        style={{ 
          boxShadow: shadowsSmall,
          animationDuration: `${50 / speed}s`
        }}
      >
        <div 
          className="absolute top-[2000px] w-[1px] h-[1px] bg-transparent"
          style={{ boxShadow: shadowsSmall }}
        />
      </div>

      {/* Stars Layer 2 (Medium) */}
      <div 
        className="absolute left-0 top-0 w-[2px] h-[2px] bg-transparent z-10 animate-[animStar_100s_linear_infinite]"
        style={{ 
          boxShadow: shadowsMedium,
          animationDuration: `${100 / speed}s`
        }}
      >
        <div 
          className="absolute top-[2000px] w-[2px] h-[2px] bg-transparent"
          style={{ boxShadow: shadowsMedium }}
        />
      </div>

      {/* Stars Layer 3 (Big) */}
      <div 
        className="absolute left-0 top-0 w-[3px] h-[3px] bg-transparent z-10 animate-[animStar_150s_linear_infinite]"
        style={{ 
          boxShadow: shadowsBig,
          animationDuration: `${150 / speed}s`
        }}
      >
        <div 
          className="absolute top-[2000px] w-[3px] h-[3px] bg-transparent"
          style={{ boxShadow: shadowsBig }}
        />
      </div>

      {/* Title Content */}
      <div className="absolute top-1/2 left-0 right-0 -mt-[60px] text-center z-20 px-4">
        <h1 className="font-light text-[30px] md:text-[50px] tracking-[10px] text-white leading-tight">
          {title.split('\n').map((line, i) => (
            <React.Fragment key={i}>
              <span className={i === 0 ? "text-gradient-clip" : "text-gradient-clip"}>
                {line}
              </span>
              {i < title.split('\n').length - 1 && <br />}
            </React.Fragment>
          ))}
        </h1>
        {children && <div className="mt-8">{children}</div>}
      </div>
    </div>
  );
}

export default ParallaxStarsBackground;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design

Here is the reference implementation of a gradient background

~~~/README.md
# Pastel Gradient Background

A dreamy, animated background component featuring rotating conic gradients and soft blur effects.

## Features

- 🎨 **Soft Pastel Palette**: Uses a carefully selected range of pastel colors (pink, peach, yellow, mint, blue, lavender).
- 🔄 **Double Rotation**: Two layers rotating in opposite directions for depth and dynamic movement.
- 🌫️ **Glassmorphism Ready**: Creates a perfect backdrop for frosted glass UI elements.
- 📱 **Responsive**: Fills the container or viewport completely.

## Usage

```tsx
import { PastelGradientBackground } from '@/sd-components/2846c5a3-16f5-428d-ba75-6752c5d018d9';

export default function MyPage() {
  return (
    <PastelGradientBackground>
      <div className="flex items-center justify-center h-screen">
        <h1 className="text-4xl font-bold">Hello World</h1>
      </div>
    </PastelGradientBackground>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| children | ReactNode | - | The content to render on top of the background |
| className | string | - | Additional classes for the wrapper div |
| ...props | HTMLAttributes | - | Standard div attributes |
~~~

~~~/src/App.tsx
import React from 'react';
import { PastelGradientBackground } from './Component';

export default function App() {
  return (
    <PastelGradientBackground />
  );
}
~~~

~~~/package.json
{
  "name": "pastel-gradient-background",
  "version": "1.0.0",
  "description": "A soft, rotating pastel gradient background with blur effects",
  "main": "src/Component.tsx",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  }
}
~~~

~~~/src/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
~~~

~~~/src/Component.tsx
import React from 'react';
import { cn } from './utils';

export interface PastelGradientBackgroundProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

export function PastelGradientBackground({ 
  children, 
  className,
  ...props 
}: PastelGradientBackgroundProps) {
  return (
    <div 
      className={cn("relative w-full h-full min-h-screen overflow-hidden", className)}
      style={{
        background: 'linear-gradient(135deg, #ffe8f3, #d9f3ff)'
      }}
      {...props}
    >
      <style>
        {`
          @keyframes rotate {
            0% {
              transform: translate(-50%, -50%) rotate(0deg);
            }
            100% {
              transform: translate(-50%, -50%) rotate(360deg);
            }
          }
          @keyframes rotate-reverse {
            0% {
              transform: translate(-50%, -50%) rotate(0deg);
            }
            100% {
              transform: translate(-50%, -50%) rotate(-360deg);
            }
          }
          .pastel-bg-layer-1 {
            background: conic-gradient(
              from 0deg,
              #ff9aa2,
              #ffb7b2,
              #ffdac1,
              #e2f0cb,
              #a2e4ff,
              #c9afff,
              #ffb7b2,
              #ff9aa2
            );
            animation: rotate 8s linear infinite;
          }
          .pastel-bg-layer-2 {
            background: conic-gradient(
              from 0deg,
              #ff9aa2,
              #ffb7b2,
              #ffdac1,
              #e2f0cb,
              #a2e4ff,
              #c9afff,
              #ffb7b2,
              #ff9aa2
            );
            animation: rotate-reverse 10s linear infinite;
          }
        `}
      </style>

      {/* Container Background (Radial) */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(circle, rgba(255, 255, 255, 0.2), rgba(0, 0, 0, 0.1))'
        }}
      />

      {/* Rotating Layers */}
      <div className="absolute top-1/2 left-1/2 w-[200%] h-[200%] -translate-x-1/2 -translate-y-1/2 pointer-events-none overflow-hidden opacity-80 blur-[50px] pastel-bg-layer-1" />
      <div className="absolute top-1/2 left-1/2 w-[180%] h-[180%] -translate-x-1/2 -translate-y-1/2 pointer-events-none overflow-hidden opacity-60 blur-[50px] pastel-bg-layer-2" />

      {/* Content */}
      <div className="relative z-10 w-full h-full">
        {children}
      </div>
    </div>
  );
}

export default PastelGradientBackground;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
