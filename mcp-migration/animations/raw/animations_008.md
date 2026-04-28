You are given a task to integrate an existing React component in the codebase

~~~/README.md
# FaultyTerminalBackground

A high-performance WebGL-based CRT/Terminal background component with glitch effects, scanlines, and digital noise. Highly interactive with mouse movements and page load animations.

## Dependencies
- ogl: ^0.0.116
- react: ^18.2.0
- framer-motion: ^11.0.8
- lucide-react: ^0.344.0

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| scale | number | 1 | Scaling of the grid pattern |
| gridMul | [number, number] | [2, 1] | Grid multiplier [x, y] |
| digitSize | number | 1.5 | Size of individual digits/pixels |
| timeScale | number | 0.3 | Speed of the animation |
| pause | boolean | false | Whether to pause the animation |
| scanlineIntensity | number | 0.3 | Intensity of the scanlines (0-1) |
| glitchAmount | number | 1 | Amount of horizontal glitching (>1 for more) |
| flickerAmount | number | 1 | Amount of screen flicker (0-1) |
| noiseAmp | number | 1 | Amplitude of the background noise |
| chromaticAberration | number | 0 | Chromatic aberration distance in pixels |
| dither | number \| boolean | 0 | Dithering intensity |
| curvature | number | 0.2 | CRT screen curvature (0-1) |
| tint | string | '#ffffff' | Color tint in hex format |
| mouseReact | boolean | true | Whether to react to mouse movement |
| mouseStrength | number | 0.2 | Strength of the mouse influence |
| pageLoadAnimation | boolean | true | Whether to show an animation on mount |
| brightness | number | 1 | Overall brightness multiplier |

## Usage

```tsx
import { FaultyTerminalBackground } from '@/sd-components/19567f92-db88-493d-a6f3-13d4bc74815f';

function MyPage() {
  return (
    <div className="w-full h-screen relative">
      <FaultyTerminalBackground 
        scale={1.5}
        tint="#00ff00"
        curvature={0.1}
        glitchAmount={1.2}
      />
      <div className="relative z-10">
        <h1>Content goes here</h1>
      </div>
    </div>
  );
}
```
~~~

~~~/src/App.tsx
import React, { useState } from 'react';
import { FaultyTerminalBackground } from './Component';
import { RefreshCw, Play, Pause, Settings2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [key, setKey] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [showControls, setShowControls] = useState(false);
  
  // Example config state
  const [config, setConfig] = useState({
    scale: 1.5,
    scanlineIntensity: 1.0,
    glitchAmount: 1.2,
    curvature: 0.1,
    brightness: 1.0,
    tint: '#ffffff'
  });

  return (
    <div className="relative w-full h-screen bg-[#1A1A1B] overflow-hidden flex items-center justify-center">
      {/* Background Component */}
      <FaultyTerminalBackground 
        key={key}
        scale={config.scale}
        gridMul={[2, 1]}
        digitSize={1.2}
        timeScale={1}
        pause={isPaused}
        scanlineIntensity={config.scanlineIntensity}
        glitchAmount={config.glitchAmount}
        flickerAmount={1}
        noiseAmp={1}
        chromaticAberration={2}
        dither={0.1}
        curvature={config.curvature}
        tint={config.tint}
        mouseReact={true}
        mouseStrength={0.5}
        pageLoadAnimation={true}
        brightness={config.brightness}
        className="z-0"
      />

      {/* Showcase Overlay */}
      <div className="z-10 text-center pointer-events-none">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-white text-5xl font-mono tracking-tighter mix-blend-difference"
        >
          FAULTY TERMINAL
        </motion.h1>
      </div>

      {/* Floating Action Button (Required by Style Guide) */}
      <div className="absolute bottom-10 right-10 flex gap-4 z-20">
        <button
          onClick={() => setShowControls(!showControls)}
          className="p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-white hover:bg-white/20 transition-all shadow-2xl"
        >
          <Settings2 size={24} />
        </button>
        <button
          onClick={() => setKey(prev => prev + 1)}
          className="p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-white hover:bg-white/20 transition-all shadow-2xl flex items-center gap-2"
        >
          <RefreshCw size={24} className={key > 0 ? 'animate-spin-slow' : ''} />
          <span className="text-sm font-medium pr-2">Reply</span>
        </button>
      </div>

      {/* Mini Controller */}
      <AnimatePresence>
        {showControls && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9, x: 20 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            exit={{ opacity: 0, scale: 0.9, x: 20 }}
            className="absolute right-10 bottom-28 w-64 bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl p-6 text-white z-30"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-mono text-xs uppercase tracking-widest text-white/50">Terminal Params</h3>
              <button onClick={() => setIsPaused(!isPaused)}>
                {isPaused ? <Play size={16} /> : <Pause size={16} />}
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="space-y-1">
                <div className="flex justify-between text-[10px] uppercase text-white/40 font-mono">
                  <span>Scale</span>
                  <span>{config.scale.toFixed(1)}</span>
                </div>
                <input 
                  type="range" min="0.5" max="4" step="0.1" 
                  value={config.scale} 
                  onChange={(e) => setConfig({...config, scale: parseFloat(e.target.value)})}
                  className="w-full accent-blue-500 bg-white/10 h-1 rounded-full appearance-none"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[10px] uppercase text-white/40 font-mono">
                  <span>Glitch</span>
                  <span>{config.glitchAmount.toFixed(1)}</span>
                </div>
                <input 
                  type="range" min="0" max="5" step="0.1" 
                  value={config.glitchAmount} 
                  onChange={(e) => setConfig({...config, glitchAmount: parseFloat(e.target.value)})}
                  className="w-full accent-blue-500 bg-white/10 h-1 rounded-full appearance-none"
                />
              </div>

              <div className="space-y-1">
                <div className="flex justify-between text-[10px] uppercase text-white/40 font-mono">
                  <span>Curvature</span>
                  <span>{config.curvature.toFixed(2)}</span>
                </div>
                <input 
                  type="range" min="0" max="0.5" step="0.01" 
                  value={config.curvature} 
                  onChange={(e) => setConfig({...config, curvature: parseFloat(e.target.value)})}
                  className="w-full accent-blue-500 bg-white/10 h-1 rounded-full appearance-none"
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style>{`
        .animate-spin-slow {
          animation: spin 3s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "faulty-terminal-background",
  "description": "A CRT/Terminal-style background with glitch effects, scanlines, and digital noise.",
  "dependencies": {
    "ogl": "^0.0.116",
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
/**
 * FaultyTerminalBackground Component
 * 
 * A high-performance WebGL background using OGL.
 * Features include:
 * - CRT scanlines and flicker
 * - Barrel distortion (curvature)
 * - Glitch and chromatic aberration
 * - Interactive mouse reaction
 * - Custom tinting and brightness control
 */

import { Renderer, Program, Mesh, Color, Triangle } from 'ogl';
import React, { useEffect, useRef, useMemo, useCallback } from 'react';

type Vec2 = [number, number];

export interface FaultyTerminalProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Scaling of the grid pattern */
  scale?: number;
  /** Grid multiplier [x, y] */
  gridMul?: Vec2;
  /** Size of individual digits/pixels */
  digitSize?: number;
  /** Speed of the animation */
  timeScale?: number;
  /** Whether to pause the animation */
  pause?: boolean;
  /** Intensity of the scanlines (0-1) */
  scanlineIntensity?: number;
  /** Amount of horizontal glitching (1 is default, >1 for more) */
  glitchAmount?: number;
  /** Amount of screen flicker (0-1) */
  flickerAmount?: number;
  /** Amplitude of the background noise/fbm */
  noiseAmp?: number;
  /** Chromatic aberration distance in pixels */
  chromaticAberration?: number;
  /** Dithering intensity to prevent color banding */
  dither?: number | boolean;
  /** CRT screen curvature (0-1) */
  curvature?: number;
  /** Color tint in hex format */
  tint?: string;
  /** Whether to react to mouse movement */
  mouseReact?: boolean;
  /** Strength of the mouse influence */
  mouseStrength?: number;
  /** Device pixel ratio (defaults to auto) */
  dpr?: number;
  /** Whether to show an animation on mount */
  pageLoadAnimation?: boolean;
  /** Overall brightness multiplier */
  brightness?: number;
}

const vertexShader = `
attribute vec2 position;
attribute vec2 uv;
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const fragmentShader = `
precision mediump float;
varying vec2 vUv;
uniform float iTime;
uniform vec3  iResolution;
uniform float uScale;
uniform vec2  uGridMul;
uniform float uDigitSize;
uniform float uScanlineIntensity;
uniform float uGlitchAmount;
uniform float uFlickerAmount;
uniform float uNoiseAmp;
uniform float uChromaticAberration;
uniform float uDither;
uniform float uCurvature;
uniform vec3  uTint;
uniform vec2  uMouse;
uniform float uMouseStrength;
uniform float uUseMouse;
uniform float uPageLoadProgress;
uniform float uUsePageLoadAnimation;
uniform float uBrightness;

float time;

float hash21(vec2 p){
  p = fract(p * 234.56);
  p += dot(p, p + 34.56);
  return fract(p.x * p.y);
}

float noise(vec2 p)
{
  return sin(p.x * 10.0) * sin(p.y * (3.0 + sin(time * 0.090909))) + 0.2; 
}

mat2 rotate(float angle)
{
  float c = cos(angle);
  float s = sin(angle);
  return mat2(c, -s, s, c);
}

float fbm(vec2 p)
{
  p *= 1.1;
  float f = 0.0;
  float amp = 0.5 * uNoiseAmp;
  
  mat2 modify0 = rotate(time * 0.02);
  f += amp * noise(p);
  p = modify0 * p * 2.0;
  amp *= 0.454545;
  
  mat2 modify1 = rotate(time * 0.02);
  f += amp * noise(p);
  p = modify1 * p * 2.0;
  amp *= 0.454545;
  
  mat2 modify2 = rotate(time * 0.08);
  f += amp * noise(p);
  
  return f;
}

float pattern(vec2 p, out vec2 q, out vec2 r) {
  vec2 offset1 = vec2(1.0);
  vec2 offset0 = vec2(0.0);
  mat2 rot01 = rotate(0.1 * time);
  mat2 rot1 = rotate(0.1);
  
  q = vec2(fbm(p + offset1), fbm(rot01 * p + offset1));
  r = vec2(fbm(rot1 * q + offset0), fbm(q + offset0));
  return fbm(p + r);
}

float digit(vec2 p){
    vec2 grid = uGridMul * 15.0;
    vec2 s = floor(p * grid) / grid;
    p = p * grid;
    vec2 q, r;
    float intensity = pattern(s * 0.1, q, r) * 1.3 - 0.03;
    
    if(uUseMouse > 0.5){
        vec2 mouseWorld = uMouse * uScale;
        float distToMouse = distance(s, mouseWorld);
        float mouseInfluence = exp(-distToMouse * 8.0) * uMouseStrength * 10.0;
        intensity += mouseInfluence;
        
        float ripple = sin(distToMouse * 20.0 - iTime * 5.0) * 0.1 * mouseInfluence;
        intensity += ripple;
    }
    
    if(uUsePageLoadAnimation > 0.5){
        float cellRandom = fract(sin(dot(s, vec2(12.9898, 78.233))) * 43758.5453);
        float cellDelay = cellRandom * 0.8;
        float cellProgress = clamp((uPageLoadProgress - cellDelay) / 0.2, 0.0, 1.0);
        
        float fadeAlpha = smoothstep(0.0, 1.0, cellProgress);
        intensity *= fadeAlpha;
    }
    
    p = fract(p);
    p *= uDigitSize;
    
    float px5 = p.x * 5.0;
    float py5 = (1.0 - p.y) * 5.0;
    float x = fract(px5);
    float y = fract(py5);
    
    float i = floor(py5) - 2.0;
    float j = floor(px5) - 2.0;
    float n = i * i + j * j;
    float f = n * 0.0625;
    
    float isOn = step(0.1, intensity - f);
    float brightness = isOn * (0.2 + y * 0.8) * (0.75 + x * 0.25);
    
    return step(0.0, p.x) * step(p.x, 1.0) * step(0.0, p.y) * step(p.y, 1.0) * brightness;
}

float onOff(float a, float b, float c)
{
  return step(c, sin(iTime + a * cos(iTime * b))) * uFlickerAmount;
}

float displace(vec2 look)
{
    float y = look.y - mod(iTime * 0.25, 1.0);
    float window = 1.0 / (1.0 + 50.0 * y * y);
    return sin(look.y * 20.0 + iTime) * 0.0125 * onOff(4.0, 2.0, 0.8) * (1.0 + cos(iTime * 60.0)) * window;
}

vec3 getColor(vec2 p){
    
    float bar = step(mod(p.y + time * 20.0, 1.0), 0.2) * 0.4 + 1.0;
    bar *= uScanlineIntensity;
    
    float displacement = displace(p);
    p.x += displacement;
    if (uGlitchAmount != 1.0) {
      float extra = displacement * (uGlitchAmount - 1.0);
      p.x += extra;
    }
    float middle = digit(p);
    
    const float off = 0.002;
    float sum = digit(p + vec2(-off, -off)) + digit(p + vec2(0.0, -off)) + digit(p + vec2(off, -off)) +
                digit(p + vec2(-off, 0.0)) + digit(p + vec2(0.0, 0.0)) + digit(p + vec2(off, 0.0)) +
                digit(p + vec2(-off, off)) + digit(p + vec2(0.0, off)) + digit(p + vec2(off, off));
    
    vec3 baseColor = vec3(0.9) * middle + sum * 0.1 * vec3(1.0) * bar;
    return baseColor;
}

vec2 barrel(vec2 uv){
  vec2 c = uv * 2.0 - 1.0;
  float r2 = dot(c, c);
  c = (1.0 + uCurvature * r2) * c;
  return c * 0.5 + 0.5;
}

void main() {
    time = iTime * 0.333333;
    vec2 uv = vUv;
    if(uCurvature != 0.0){
      uv = barrel(uv);
    }
    
    vec2 p = uv * uScale;
    vec3 col = getColor(p);
    if(uChromaticAberration != 0.0){
      vec2 ca = vec2(uChromaticAberration) / iResolution.xy;
      col.r = getColor(p + ca).r;
      col.b = getColor(p - ca).b;
    }
    col *= uTint;
    col *= uBrightness;
    if(uDither > 0.0){
      float rnd = hash21(gl_FragCoord.xy);
      col += (rnd - 0.5) * (uDither * 0.003922);
    }
    gl_FragColor = vec4(col, 1.0);
}
`;

function hexToRgb(hex: string): [number, number, number] {
  let h = hex.replace('#', '').trim();
  if (h.length === 3)
    h = h
      .split('')
      .map(c => c + c)
      .join('');
  const num = parseInt(h, 16);
  return [((num >> 16) & 255) / 255, ((num >> 8) & 255) / 255, (num & 255) / 255];
}

export function FaultyTerminalBackground({
  scale = 1,
  gridMul = [2, 1],
  digitSize = 1.5,
  timeScale = 0.3,
  pause = false,
  scanlineIntensity = 0.3,
  glitchAmount = 1,
  flickerAmount = 1,
  noiseAmp = 1,
  chromaticAberration = 0,
  dither = 0,
  curvature = 0.2,
  tint = '#ffffff',
  mouseReact = true,
  mouseStrength = 0.2,
  dpr = Math.min(typeof window !== 'undefined' ? window.devicePixelRatio : 1, 2),
  pageLoadAnimation = true,
  brightness = 1,
  className,
  style,
  ...rest
}: FaultyTerminalProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const programRef = useRef<Program>(null);
  const rendererRef = useRef<Renderer>(null);
  const mouseRef = useRef({ x: 0.5, y: 0.5 });
  const smoothMouseRef = useRef({ x: 0.5, y: 0.5 });
  const frozenTimeRef = useRef(0);
  const rafRef = useRef<number>(0);
  const loadAnimationStartRef = useRef<number>(0);
  const timeOffsetRef = useRef<number>(Math.random() * 100);

  const tintVec = useMemo(() => hexToRgb(tint), [tint]);
  const ditherValue = useMemo(() => (typeof dither === 'boolean' ? (dither ? 1 : 0) : dither), [dither]);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    const ctn = containerRef.current;
    if (!ctn) return;
    const rect = ctn.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = 1 - (e.clientY - rect.top) / rect.height;
    mouseRef.current = { x, y };
  }, []);

  useEffect(() => {
    const ctn = containerRef.current;
    if (!ctn) return;

    const renderer = new Renderer({ dpr });
    rendererRef.current = renderer;
    const gl = renderer.gl;
    gl.clearColor(0, 0, 0, 1);

    const geometry = new Triangle(gl);

    const program = new Program(gl, {
      vertex: vertexShader,
      fragment: fragmentShader,
      uniforms: {
        iTime: { value: 0 },
        iResolution: {
          value: new Color(gl.canvas.width, gl.canvas.height, gl.canvas.width / gl.canvas.height)
        },
        uScale: { value: scale },
        uGridMul: { value: new Float32Array(gridMul) },
        uDigitSize: { value: digitSize },
        uScanlineIntensity: { value: scanlineIntensity },
        uGlitchAmount: { value: glitchAmount },
        uFlickerAmount: { value: flickerAmount },
        uNoiseAmp: { value: noiseAmp },
        uChromaticAberration: { value: chromaticAberration },
        uDither: { value: ditherValue },
        uCurvature: { value: curvature },
        uTint: { value: new Color(tintVec[0], tintVec[1], tintVec[2]) },
        uMouse: {
          value: new Float32Array([smoothMouseRef.current.x, smoothMouseRef.current.y])
        },
        uMouseStrength: { value: mouseStrength },
        uUseMouse: { value: mouseReact ? 1 : 0 },
        uPageLoadProgress: { value: pageLoadAnimation ? 0 : 1 },
        uUsePageLoadAnimation: { value: pageLoadAnimation ? 1 : 0 },
        uBrightness: { value: brightness }
      }
    });

    programRef.current = program;
    const mesh = new Mesh(gl, { geometry, program });

    function resize() {
      if (!ctn || !renderer) return;
      renderer.setSize(ctn.offsetWidth, ctn.offsetHeight);
      program.uniforms.iResolution.value = new Color(
        gl.canvas.width,
        gl.canvas.height,
        gl.canvas.width / gl.canvas.height
      );
    }

    const resizeObserver = new ResizeObserver(() => resize());
    resizeObserver.observe(ctn);
    resize();

    const update = (t: number) => {
      rafRef.current = requestAnimationFrame(update);

      if (pageLoadAnimation && loadAnimationStartRef.current === 0) {
        loadAnimationStartRef.current = t;
      }

      if (!pause) {
        const elapsed = (t * 0.001 + timeOffsetRef.current) * timeScale;
        program.uniforms.iTime.value = elapsed;
        frozenTimeRef.current = elapsed;
      } else {
        program.uniforms.iTime.value = frozenTimeRef.current;
      }

      if (pageLoadAnimation && loadAnimationStartRef.current > 0) {
        const animationDuration = 2000;
        const animationElapsed = t - loadAnimationStartRef.current;
        const progress = Math.min(animationElapsed / animationDuration, 1);
        program.uniforms.uPageLoadProgress.value = progress;
      }

      if (mouseReact) {
        const dampingFactor = 0.08;
        const smoothMouse = smoothMouseRef.current;
        const mouse = mouseRef.current;
        smoothMouse.x += (mouse.x - smoothMouse.x) * dampingFactor;
        smoothMouse.y += (mouse.y - smoothMouse.y) * dampingFactor;
        const mouseUniform = program.uniforms.uMouse.value as Float32Array;
        mouseUniform[0] = smoothMouse.x;
        mouseUniform[1] = smoothMouse.y;
      }

      renderer.render({ scene: mesh });
    };

    rafRef.current = requestAnimationFrame(update);
    ctn.appendChild(gl.canvas);

    if (mouseReact) ctn.addEventListener('mousemove', handleMouseMove);

    return () => {
      cancelAnimationFrame(rafRef.current);
      resizeObserver.disconnect();
      if (mouseReact) ctn.removeEventListener('mousemove', handleMouseMove);
      if (gl.canvas.parentElement === ctn) ctn.removeChild(gl.canvas);
      gl.getExtension('WEBGL_lose_context')?.loseContext();
      loadAnimationStartRef.current = 0;
    };
  }, [
    dpr,
    pause,
    timeScale,
    scale,
    gridMul,
    digitSize,
    scanlineIntensity,
    glitchAmount,
    flickerAmount,
    noiseAmp,
    chromaticAberration,
    ditherValue,
    curvature,
    tintVec,
    mouseReact,
    mouseStrength,
    pageLoadAnimation,
    brightness,
    handleMouseMove
  ]);

  return (
    <div
      ref={containerRef}
      className={`w-full h-full relative overflow-hidden bg-background ${className}`}
      style={style}
      {...rest}
    />
  );
}

export default FaultyTerminalBackground;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
