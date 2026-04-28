You are given a task to integrate an existing React component in the codebase

~~~/README.md
# RibbonShowcase

A premium minimalist showcase of an interactive ribbon effect using OGL (WebGL). This component features fluid, spring-based motion that follows mouse or touch movements, creating an atmospheric and high-end visual experience.

## Dependencies

- `ogl`: ^0.0.117
- `framer-motion`: ^11.11.17
- `react`: ^18.3.1
- `react-dom`: ^18.3.1

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `colors` | `string[]` | `['#ff9346', '#7cff67', '#ffee51', '#5227FF']` | Array of hex color strings for the ribbons |
| `baseSpring` | `number` | `0.03` | Spring tension for movement (lower = more fluid) |
| `baseFriction` | `number` | `0.9` | Friction for movement (lower = more drift) |
| `baseThickness` | `number` | `30` | Thickness of the ribbons in pixels |
| `offsetFactor` | `number` | `0.05` | Horizontal offset factor between multiple ribbons |
| `maxAge` | `number` | `500` | Max lifetime/length of the trail |
| `pointCount` | `number` | `50` | Number of points defining each ribbon curve |
| `speedMultiplier` | `number` | `0.6` | Speed multiplier for movement interpolation |
| `enableFade` | `boolean` | `false` | Enable transparency fade at the end of the ribbon |
| `enableShaderEffect` | `boolean` | `false` | Enable wave-like shader distortion effect |
| `effectAmplitude` | `number` | `2` | Amplitude of the shader distortion |
| `backgroundColor` | `number[]` | `[0, 0, 0, 0]` | Background clear color [r, g, b, a] |

## Usage Example

```tsx
import { Ribbons } from '@/sd-components/b8472475-8adc-4656-b93e-725ce5e30657';

export default function MyComponent() {
  return (
    <div style={{ height: '500px', width: '100%', position: 'relative' }}>
      <Ribbons
        baseThickness={40}
        colors={['#1A1A1B']}
        speedMultiplier={0.5}
        maxAge={600}
        enableFade={true}
        enableShaderEffect={true}
        effectAmplitude={1.5}
      />
    </div>
  );
}
```
~~~

~~~/src/App.tsx
/**
 * RibbonShowcase Demo
 * Displays the Ribbons component in a premium, minimalist framing.
 * Adheres to the 'Minimalist Showcase' style guide:
 * - Off-white background (#F9F9F9)
 * - Ample whitespace
 * - Floating soft-shadow container
 * - Monochrome palette with a single brand accent
 */

import React, { useState } from 'react';
import { Ribbons } from './Component';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div className="min-h-screen bg-[#F9F9F9] flex items-center justify-center p-20 font-sans">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.19, 1, 0.22, 1] }}
        className="relative w-full max-w-4xl aspect-video bg-white rounded-[2rem] shadow-[0_40px_80px_rgba(0,0,0,0.05)] overflow-hidden border-none"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        {/* The Animated Element */}
        <div className="absolute inset-0 z-0">
          <Ribbons
            baseThickness={40}
            colors={['#1A1A1B']} // Monochrome base
            speedMultiplier={0.5}
            maxAge={600}
            enableFade={true}
            enableShaderEffect={true}
            effectAmplitude={1.5}
            backgroundColor={[0, 0, 0, 0]}
          />
        </div>

        {/* Content Overlay */}
        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center pointer-events-none p-12 text-center">
          <motion.h1 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="text-[2.5rem] font-medium tracking-tight text-[#1A1A1B] mb-2"
          >
            Fluid Motion
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-[#888888] font-normal"
          >
            A Minimalist WebGL Ribbon Showcase
          </motion.p>
        </div>

        {/* Reply Button (Required by prompt for animations) */}
        <AnimatePresence>
          {isHovered && (
            <motion.button
              initial={{ opacity: 0, scale: 0.9, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 10 }}
              transition={{ duration: 0.3, ease: [0.19, 1, 0.22, 1] }}
              onClick={() => window.location.reload()}
              className="absolute bottom-8 right-8 z-20 px-6 py-3 bg-[#1A1A1B] text-white rounded-full text-sm font-medium shadow-lg hover:bg-black transition-colors pointer-events-auto flex items-center gap-2 group"
            >
              <svg 
                width="16" 
                height="16" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2.5" 
                strokeLinecap="round" 
                strokeLinejoin="round"
                className="group-hover:rotate-[-180deg] transition-transform duration-500"
              >
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
                <path d="M3 3v5h5" />
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" />
                <path d="M16 16h5v5" />
              </svg>
              Reply Animation
            </motion.button>
          )}
        </AnimatePresence>

        {/* Interactive Highlight (Single brand accent) */}
        <motion.div 
          className="absolute bottom-0 left-0 h-1 bg-black w-full origin-left"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: isHovered ? 1 : 0 }}
          transition={{ duration: 0.6, ease: [0.19, 1, 0.22, 1] }}
        />
      </motion.div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "ribbon-showcase",
  "description": "A premium WebGL interactive ribbon effect showcase.",
  "dependencies": {
    "ogl": "^0.0.117",
    "framer-motion": "^11.11.17",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.460.0"
  }
}
~~~

~~~/src/Component.tsx
/**
 * Ribbons Component
 * A WebGL-powered interactive ribbon effect using the OGL library.
 * Features fluid, spring-based motion that follows the mouse/touch position.
 * Optimized for performance with customizable thickness, speed, and shader effects.
 */

import React, { useEffect, useRef } from 'react';
import { Renderer, Transform, Vec3, Color, Polyline } from 'ogl';

interface RibbonsProps {
  /** Array of hex color strings for the ribbons */
  colors?: string[];
  /** Spring tension for the movement (lower = more fluid) */
  baseSpring?: number;
  /** Friction for the movement (lower = more drift) */
  baseFriction?: number;
  /** Thickness of the ribbons in pixels */
  baseThickness?: number;
  /** Horizontal offset factor between multiple ribbons */
  offsetFactor?: number;
  /** Max lifetime/length of the trail */
  maxAge?: number;
  /** Number of points defining each ribbon curve */
  pointCount?: number;
  /** Speed multiplier for movement interpolation */
  speedMultiplier?: number;
  /** Enable transparency fade at the end of the ribbon */
  enableFade?: boolean;
  /** Enable wave-like shader distortion effect */
  enableShaderEffect?: boolean;
  /** Amplitude of the shader distortion */
  effectAmplitude?: number;
  /** Background clear color [r, g, b, a] */
  backgroundColor?: number[];
}

export const Ribbons: React.FC<RibbonsProps> = ({
  colors = ['#ff9346', '#7cff67', '#ffee51', '#5227FF'],
  baseSpring = 0.03,
  baseFriction = 0.9,
  baseThickness = 30,
  offsetFactor = 0.05,
  maxAge = 500,
  pointCount = 50,
  speedMultiplier = 0.6,
  enableFade = false,
  enableShaderEffect = false,
  effectAmplitude = 2,
  backgroundColor = [0, 0, 0, 0]
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const renderer = new Renderer({ dpr: window.devicePixelRatio || 2, alpha: true });
    const gl = renderer.gl;

    if (Array.isArray(backgroundColor) && backgroundColor.length === 4) {
      gl.clearColor(backgroundColor[0], backgroundColor[1], backgroundColor[2], backgroundColor[3]);
    } else {
      gl.clearColor(0, 0, 0, 0);
    }

    gl.canvas.style.position = 'absolute';
    gl.canvas.style.top = '0';
    gl.canvas.style.left = '0';
    gl.canvas.style.width = '100%';
    gl.canvas.style.height = '100%';
    container.appendChild(gl.canvas);

    const scene = new Transform();
    const lines: {
      spring: number;
      friction: number;
      mouseVelocity: Vec3;
      mouseOffset: Vec3;
      points: Vec3[];
      polyline: Polyline;
    }[] = [];

    const vertex = `
      precision highp float;
      
      attribute vec3 position;
      attribute vec3 next;
      attribute vec3 prev;
      attribute vec2 uv;
      attribute float side;
      
      uniform vec2 uResolution;
      uniform float uDPR;
      uniform float uThickness;
      uniform float uTime;
      uniform float uEnableShaderEffect;
      uniform float uEffectAmplitude;
      
      varying vec2 vUV;
      
      vec4 getPosition() {
          vec4 current = vec4(position, 1.0);
          vec2 aspect = vec2(uResolution.x / uResolution.y, 1.0);
          vec2 nextScreen = next.xy * aspect;
          vec2 prevScreen = prev.xy * aspect;
          vec2 tangent = normalize(nextScreen - prevScreen);
          vec2 normal = vec2(-tangent.y, tangent.x);
          normal /= aspect;
          normal *= mix(1.0, 0.1, pow(abs(uv.y - 0.5) * 2.0, 2.0));
          float dist = length(nextScreen - prevScreen);
          normal *= smoothstep(0.0, 0.02, dist);
          float pixelWidthRatio = 1.0 / (uResolution.y / uDPR);
          float pixelWidth = current.w * pixelWidthRatio;
          normal *= pixelWidth * uThickness;
          current.xy -= normal * side;
          if(uEnableShaderEffect > 0.5) {
            current.xy += normal * sin(uTime + current.x * 10.0) * uEffectAmplitude;
          }
          return current;
      }
      
      void main() {
          vUV = uv;
          gl_Position = getPosition();
      }
    `;

    const fragment = `
      precision highp float;
      uniform vec3 uColor;
      uniform float uOpacity;
      uniform float uEnableFade;
      varying vec2 vUV;
      void main() {
          float fadeFactor = 1.0;
          if(uEnableFade > 0.5) {
              fadeFactor = 1.0 - smoothstep(0.0, 1.0, vUV.y);
          }
          gl_FragColor = vec4(uColor, uOpacity * fadeFactor);
      }
    `;

    function resize() {
      if (!container) return;
      const width = container.clientWidth;
      const height = container.clientHeight;
      renderer.setSize(width, height);
      lines.forEach(line => line.polyline.resize());
    }

    window.addEventListener('resize', resize);

    const center = (colors.length - 1) / 2;
    colors.forEach((color, index) => {
      const spring = baseSpring + (Math.random() - 0.5) * 0.05;
      const friction = baseFriction + (Math.random() - 0.5) * 0.05;
      const thickness = baseThickness + (Math.random() - 0.5) * 3;
      const mouseOffset = new Vec3(
        (index - center) * offsetFactor + (Math.random() - 0.5) * 0.01,
        (Math.random() - 0.5) * 0.1,
        0
      );

      const line = {
        spring,
        friction,
        mouseVelocity: new Vec3(),
        mouseOffset,
        points: [] as Vec3[],
        polyline: {} as Polyline
      };

      const count = pointCount;
      const points: Vec3[] = [];
      for (let i = 0; i < count; i++) {
        points.push(new Vec3());
      }
      line.points = points;
      line.polyline = new Polyline(gl, {
        points,
        vertex,
        fragment,
        uniforms: {
          uColor: { value: new Color(color) },
          uThickness: { value: thickness },
          uOpacity: { value: 1.0 },
          uTime: { value: 0.0 },
          uEnableShaderEffect: { value: enableShaderEffect ? 1.0 : 0.0 },
          uEffectAmplitude: { value: effectAmplitude },
          uEnableFade: { value: enableFade ? 1.0 : 0.0 }
        }
      });
      line.polyline.mesh.setParent(scene);
      lines.push(line);
    });

    resize();

    const mouse = new Vec3();
    function updateMouse(e: MouseEvent | TouchEvent) {
      let x: number, y: number;
      if (!container) return;
      const rect = container.getBoundingClientRect();
      if ('changedTouches' in e && e.changedTouches.length) {
        x = e.changedTouches[0].clientX - rect.left;
        y = e.changedTouches[0].clientY - rect.top;
      } else if (e instanceof MouseEvent) {
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
      } else {
        x = 0;
        y = 0;
      }
      const width = container.clientWidth;
      const height = container.clientHeight;
      mouse.set((x / width) * 2 - 1, (y / height) * -2 + 1, 0);
    }

    container.addEventListener('mousemove', updateMouse);
    container.addEventListener('touchstart', updateMouse, { passive: false });
    container.addEventListener('touchmove', updateMouse, { passive: false });

    let frameId: number;
    let lastTime = performance.now();

    function update() {
      frameId = requestAnimationFrame(update);
      const currentTime = performance.now();
      const dt = currentTime - lastTime;
      lastTime = currentTime;

      lines.forEach(line => {
        const tmp = new Vec3();
        tmp.copy(mouse).add(line.mouseOffset).sub(line.points[0]).multiply(line.spring);
        line.mouseVelocity.add(tmp).multiply(line.friction);
        line.points[0].add(line.mouseVelocity);

        for (let i = 1; i < line.points.length; i++) {
          if (isFinite(maxAge) && maxAge > 0) {
            const segmentDelay = maxAge / (line.points.length - 1);
            const alpha = Math.min(1, (dt * speedMultiplier) / segmentDelay);
            line.points[i].lerp(line.points[i - 1], alpha);
          } else {
            line.points[i].lerp(line.points[i - 1], 0.9);
          }
        }

        if (line.polyline.mesh.program.uniforms.uTime) {
          line.polyline.mesh.program.uniforms.uTime.value = currentTime * 0.001;
        }
        line.polyline.updateGeometry();
      });

      renderer.render({ scene });
    }

    update();

    return () => {
      window.removeEventListener('resize', resize);
      container.removeEventListener('mousemove', updateMouse);
      container.removeEventListener('touchstart', updateMouse);
      container.removeEventListener('touchmove', updateMouse);
      cancelAnimationFrame(frameId);
      if (gl.canvas && gl.canvas.parentNode === container) {
        container.removeChild(gl.canvas);
      }
    };
  }, [
    colors,
    baseSpring,
    baseFriction,
    baseThickness,
    offsetFactor,
    maxAge,
    pointCount,
    speedMultiplier,
    enableFade,
    enableShaderEffect,
    effectAmplitude,
    backgroundColor
  ]);

  return <div ref={containerRef} className="relative w-full h-full cursor-none" />;
};

export default Ribbons;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
