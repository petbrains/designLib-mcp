You are given a task to integrate an existing React component in the codebase

~~~/README.md
# Plasma Showcase

A mesmerizing, high-performance plasma background effect built with React and WebGL (via OGL). This component creates a fluid, organic motion pattern that is highly customizable and responsive to mouse interaction.

## Dependencies
- `ogl`: ^1.0.11
- `framer-motion`: ^11.11.11
- `lucide-react`: ^0.454.0

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | `string` | `"#ffffff"` | Hex color used to tint the plasma effect. |
| `speed` | `number` | `1` | Multiplier for animation speed. |
| `direction` | `'forward' \| 'reverse' \| 'pingpong'` | `'forward'` | Controls the temporal flow of the animation. |
| `scale` | `number` | `1` | Zoom level of the plasma patterns. |
| `opacity` | `number` | `1` | Global transparency of the rendered output. |
| `mouseInteractive` | `boolean` | `true` | Enables subtle parallax distortion based on mouse position. |

## Usage
```tsx
import { Plasma } from '@/sd-components/f6c4c92e-8c58-4d24-bca2-b50e4c917a8e';

function MyView() {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <Plasma 
        color="#ff6b35"
        speed={0.6}
        mouseInteractive={true}
      />
    </div>
  );
}
```
~~~

~~~/src/App.tsx
/**
 * Demo for Plasma component.
 * Showcases a single mesmerizing instance of the Plasma effect in a minimalist container.
 */

import React from 'react';
import { Plasma } from './Component';
import { RefreshCcw } from 'lucide-react';
import { motion } from 'framer-motion';

export default function App() {
  const [key, setKey] = React.useState(0);

  return (
    <div className="min-h-screen w-full bg-[#1A1A1B] flex items-center justify-center p-20">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="relative w-full max-w-4xl aspect-video rounded-[32px] overflow-hidden shadow-[0_40px_100px_rgba(0,0,0,0.3)] bg-black border border-white/5 group"
      >
        <Plasma 
          key={key}
          color="#ff6b35"
          speed={0.6}
          direction="forward"
          scale={1.1}
          opacity={0.8}
          mouseInteractive={true}
        />
        
        {/* Title Overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <motion.h1 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="text-white text-3xl font-medium tracking-tight mb-2"
          >
            Plasma Animation
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.6 }}
            className="text-white/40 text-sm font-normal"
          >
            High-performance WebGL Fluidity
          </motion.p>
        </div>

        {/* Reply/Reset Button */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setKey(prev => prev + 1)}
          className="absolute bottom-8 right-8 w-12 h-12 bg-white/10 backdrop-blur-md rounded-full flex items-center justify-center shadow-lg border border-white/10 transition-colors hover:bg-white/20 pointer-events-auto"
        >
          <RefreshCcw className="w-5 h-5 text-white" />
        </motion.button>
      </motion.div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "plasma-showcase",
  "description": "A mesmerizing, high-performance plasma background effect using OGL.",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "ogl": "^1.0.11",
    "lucide-react": "^0.454.0",
    "framer-motion": "^11.11.11"
  }
}
~~~

~~~/src/Component.tsx
/**
 * Plasma Background Component
 * A high-performance WebGL shader effect using OGL.
 * Features customizable colors, speed, scale, and interactivity.
 */

import React, { useEffect, useRef } from 'react';
import { Renderer, Program, Mesh, Triangle } from 'ogl';

export interface PlasmaProps {
  /** Accent color for the plasma effect. Defaults to #ffffff. */
  color?: string;
  /** Speed of the animation loop. Defaults to 1. */
  speed?: number;
  /** Direction of the flow. Defaults to 'forward'. */
  direction?: 'forward' | 'reverse' | 'pingpong';
  /** Scale factor for the shader patterns. Defaults to 1. */
  scale?: number;
  /** Overall opacity of the effect. Defaults to 1. */
  opacity?: number;
  /** Whether the effect responds to mouse movement. Defaults to true. */
  mouseInteractive?: boolean;
}

const hexToRgb = (hex: string): [number, number, number] => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  if (!result) return [1, 0.5, 0.2];
  return [parseInt(result[1], 16) / 255, parseInt(result[2], 16) / 255, parseInt(result[3], 16) / 255];
};

const vertex = `#version 300 es
precision highp float;
in vec2 position;
in vec2 uv;
out vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const fragment = `#version 300 es
precision highp float;
uniform vec2 iResolution;
uniform float iTime;
uniform vec3 uCustomColor;
uniform float uUseCustomColor;
uniform float uSpeed;
uniform float uDirection;
uniform float uScale;
uniform float uOpacity;
uniform vec2 uMouse;
uniform float uMouseInteractive;
out vec4 fragColor;

void mainImage(out vec4 o, vec2 C) {
  vec2 center = iResolution.xy * 0.5;
  C = (C - center) / uScale + center;
  
  vec2 mouseOffset = (uMouse - center) * 0.0002;
  C += mouseOffset * length(C - center) * step(0.5, uMouseInteractive);
  
  float i, d, z, T = iTime * uSpeed * uDirection;
  vec3 O, p, S;
  for (vec2 r = iResolution.xy, Q; ++i < 60.; O += o.w/d*o.xyz) {
    p = z*normalize(vec3(C-.5*r,r.y)); 
    p.z -= 4.; 
    S = p;
    d = p.y-T;
    
    p.x += .4*(1.+p.y)*sin(d + p.x*0.1)*cos(.34*d + p.x*0.05); 
    Q = p.xz *= mat2(cos(p.y+vec4(0,11,33,0)-T)); 
    z+= d = abs(sqrt(length(Q*Q)) - .25*(5.+S.y))/3.+8e-4; 
    o = 1.+sin(S.y+p.z*.5+S.z-length(S-p)+vec4(2,1,0,8));
  }
  
  o.xyz = tanh(O/1e4);
}

bool finite1(float x){ return !(isnan(x) || isinf(x)); }
vec3 sanitize(vec3 c){
  return vec3(
    finite1(c.r) ? c.r : 0.0,
    finite1(c.g) ? c.g : 0.0,
    finite1(c.b) ? c.b : 0.0
  );
}

void main() {
  vec4 o = vec4(0.0);
  mainImage(o, gl_FragCoord.xy);
  vec3 rgb = sanitize(o.rgb);
  
  float intensity = (rgb.r + rgb.g + rgb.b) / 3.0;
  vec3 customColor = intensity * uCustomColor;
  vec3 finalColor = mix(rgb, customColor, step(0.5, uUseCustomColor));
  
  float alpha = length(rgb) * uOpacity;
  fragColor = vec4(finalColor, alpha);
}`;

export const Plasma: React.FC<PlasmaProps> = ({
  color = '#ffffff',
  speed = 1,
  direction = 'forward',
  scale = 1,
  opacity = 1,
  mouseInteractive = true
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mousePos = useRef({ x: 0, y: 0 });

  useEffect(() => {
    if (!containerRef.current) return;

    const useCustomColor = color ? 1.0 : 0.0;
    const customColorRgb = color ? hexToRgb(color) : [1, 1, 1];
    const directionMultiplier = direction === 'reverse' ? -1.0 : 1.0;

    const renderer = new Renderer({
      webgl: 2,
      alpha: true,
      antialias: false,
      dpr: Math.min(window.devicePixelRatio || 1, 2)
    });

    const gl = renderer.gl;
    const canvas = gl.canvas as HTMLCanvasElement;
    canvas.style.display = 'block';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    containerRef.current.appendChild(canvas);

    const geometry = new Triangle(gl);
    const program = new Program(gl, {
      vertex: vertex,
      fragment: fragment,
      uniforms: {
        iTime: { value: 0 },
        iResolution: { value: new Float32Array([1, 1]) },
        uCustomColor: { value: new Float32Array(customColorRgb) },
        uUseCustomColor: { value: useCustomColor },
        uSpeed: { value: speed * 0.4 },
        uDirection: { value: directionMultiplier },
        uScale: { value: scale },
        uOpacity: { value: opacity },
        uMouse: { value: new Float32Array([0, 0]) },
        uMouseInteractive: { value: mouseInteractive ? 1.0 : 0.0 }
      }
    });

    const mesh = new Mesh(gl, { geometry, program });

    const handleMouseMove = (e: MouseEvent) => {
      if (!mouseInteractive || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      mousePos.current.x = e.clientX - rect.left;
      mousePos.current.y = e.clientY - rect.top;
      const mouseUniform = program.uniforms.uMouse.value as Float32Array;
      mouseUniform[0] = mousePos.current.x;
      mouseUniform[1] = mousePos.current.y;
    };

    if (mouseInteractive) {
      containerRef.current.addEventListener('mousemove', handleMouseMove);
    }

    const setSize = () => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const width = Math.max(1, Math.floor(rect.width));
      const height = Math.max(1, Math.floor(rect.height));
      renderer.setSize(width, height);
      const res = program.uniforms.iResolution.value as Float32Array;
      res[0] = gl.drawingBufferWidth;
      res[1] = gl.drawingBufferHeight;
    };

    const ro = new ResizeObserver(setSize);
    ro.observe(containerRef.current);
    setSize();

    let raf = 0;
    const t0 = performance.now();
    const loop = (t: number) => {
      let timeValue = (t - t0) * 0.001;
      if (direction === 'pingpong') {
        const pingpongDuration = 10;
        const segmentTime = timeValue % (pingpongDuration * 2);
        const pingpongTime = segmentTime > pingpongDuration 
          ? (pingpongDuration * 2 - segmentTime) 
          : segmentTime;
        (program.uniforms.iTime as any).value = pingpongTime;
      } else {
        (program.uniforms.iTime as any).value = timeValue;
      }
      renderer.render({ scene: mesh });
      raf = requestAnimationFrame(loop);
    };

    raf = requestAnimationFrame(loop);

    return () => {
      cancelAnimationFrame(raf);
      ro.disconnect();
      if (mouseInteractive && containerRef.current) {
        containerRef.current.removeEventListener('mousemove', handleMouseMove);
      }
      try {
        if (containerRef.current && canvas.parentNode === containerRef.current) {
          containerRef.current.removeChild(canvas);
        }
      } catch (err) {
        console.warn('Plasma cleanup failed:', err);
      }
    };
  }, [color, speed, direction, scale, opacity, mouseInteractive]);

  return <div ref={containerRef} className="w-full h-full relative overflow-hidden" />;
};

export default Plasma;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
