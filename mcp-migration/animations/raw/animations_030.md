You are given a task to integrate an existing React component in the codebase

~~~/README.md
# ShinyText

A text component with a customizable shining gradient animation effect that sweeps across the text.

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | string | - | The text to display and animate |
| `disabled` | boolean | false | Whether to disable the animation |
| `speed` | number | 2 | Duration of the animation in seconds |
| `className` | string | '' | Additional CSS classes for styling |
| `color` | string | '#b5b5b5' | The base color of the text |
| `shineColor` | string | '#ffffff' | The color of the shine effect |
| `spread` | number | 120 | The spread angle of the gradient in degrees |
| `yoyo` | boolean | false | Whether the animation should bounce back and forth |
| `pauseOnHover` | boolean | false | Whether to pause the animation on hover |
| `direction` | 'left' \| 'right' | 'left' | The direction of the shine movement |
| `delay` | number | 0 | Delay before animation starts (in seconds) |

## Usage

```tsx
import ShinyText from '@/sd-components/2f78ed51-fbb9-4da5-8537-b528a39fe26f';

// Basic usage
<ShinyText text="Just some shiny text!" />

// Custom speed and colors
<ShinyText 
  text="Shiny Text" 
  disabled={false}
  speed={3} 
  className="custom-class" 
  color="#888888"
  shineColor="#3b82f6" 
/>

// Interactive usage
<ShinyText 
  text="Hover to pause" 
  pauseOnHover={true}
  speed={1.5}
/>
```
~~~

~~~/src/App.tsx
import React from 'react';
import ShinyText from './ShinyText';

export default function App() {
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-[#1A1A1B] p-8 font-sans">
      <div className="relative group rounded-3xl bg-[#222224] p-16 shadow-[0_0_40px_rgba(0,0,0,0.3)] transition-all hover:shadow-[0_0_60px_rgba(0,0,0,0.5)] border border-white/5">
        <div className="text-center space-y-12">
            <div>
              <h2 className="text-sm font-medium text-white/40 mb-8 uppercase tracking-[0.2em]">Default Animation</h2>
              <div className="text-4xl md:text-5xl font-bold tracking-tight">
                  <ShinyText 
                      text="✨ Shiny Text Effect" 
                      disabled={false}
                      speed={3} 
                      className="custom-class" 
                  />
              </div>
            </div>
            
             <div className="pt-12 border-t border-white/5 grid gap-8 justify-items-center">
                <div>
                  <p className="text-xs text-white/30 mb-4 uppercase tracking-widest">Hover to Pause</p>
                  <ShinyText 
                      text="Hover over me to pause the shine" 
                      speed={2} 
                      color="#888888"
                      shineColor="#3b82f6" // Electric blue
                      className="text-xl font-medium"
                      pauseOnHover={true}
                  />
                </div>
                
                <div>
                  <p className="text-xs text-white/30 mb-4 uppercase tracking-widest">Yoyo Effect</p>
                   <ShinyText 
                      text="Bouncing back and forth" 
                      speed={1.5} 
                      color="#888888"
                      shineColor="#ec4899" // Pink
                      className="text-xl font-medium"
                      yoyo={true}
                  />
                </div>
            </div>
        </div>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "shiny-text-component",
  "version": "1.0.0",
  "description": "A shiny text animation component using Motion",
  "main": "src/ShinyText.tsx",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "motion": "^12.0.0",
    "lucide-react": "^0.344.0"
  }
}
~~~

~~~/src/ShinyText.tsx
import React, { useState, useCallback, useEffect, useRef } from 'react';
import { motion, useMotionValue, useAnimationFrame, useTransform } from 'motion/react';

interface ShinyTextProps {
  text: string;
  disabled?: boolean;
  speed?: number;
  className?: string;
  color?: string;
  shineColor?: string;
  spread?: number;
  yoyo?: boolean;
  pauseOnHover?: boolean;
  direction?: 'left' | 'right';
  delay?: number;
}

const ShinyText: React.FC<ShinyTextProps> = ({
  text,
  disabled = false,
  speed = 2,
  className = '',
  color = '#b5b5b5',
  shineColor = '#ffffff',
  spread = 120,
  yoyo = false,
  pauseOnHover = false,
  direction = 'left',
  delay = 0
}) => {
  const [isPaused, setIsPaused] = useState(false);
  const progress = useMotionValue(0);
  const elapsedRef = useRef(0);
  const lastTimeRef = useRef<number | null>(null);
  const directionRef = useRef(direction === 'left' ? 1 : -1);

  const animationDuration = speed * 1000;
  const delayDuration = delay * 1000;

  useAnimationFrame(time => {
    if (disabled || isPaused) {
      lastTimeRef.current = null;
      return;
    }

    if (lastTimeRef.current === null) {
      lastTimeRef.current = time;
      return;
    }

    const deltaTime = time - lastTimeRef.current;
    lastTimeRef.current = time;
    elapsedRef.current += deltaTime;

    // Animation goes from 0 to 100
    if (yoyo) {
      const cycleDuration = animationDuration + delayDuration;
      const fullCycle = cycleDuration * 2;
      const cycleTime = elapsedRef.current % fullCycle;

      if (cycleTime < animationDuration) {
        // Forward animation: 0 -> 100
        const p = (cycleTime / animationDuration) * 100;
        progress.set(directionRef.current === 1 ? p : 100 - p);
      } else if (cycleTime < cycleDuration) {
        // Delay at end
        progress.set(directionRef.current === 1 ? 100 : 0);
      } else if (cycleTime < cycleDuration + animationDuration) {
        // Reverse animation: 100 -> 0
        const reverseTime = cycleTime - cycleDuration;
        const p = 100 - (reverseTime / animationDuration) * 100;
        progress.set(directionRef.current === 1 ? p : 100 - p);
      } else {
        // Delay at start
        progress.set(directionRef.current === 1 ? 0 : 100);
      }
    } else {
      const cycleDuration = animationDuration + delayDuration;
      const cycleTime = elapsedRef.current % cycleDuration;

      if (cycleTime < animationDuration) {
        // Animation phase: 0 -> 100
        const p = (cycleTime / animationDuration) * 100;
        progress.set(directionRef.current === 1 ? p : 100 - p);
      } else {
        // Delay phase - hold at end (shine off-screen)
        progress.set(directionRef.current === 1 ? 100 : 0);
      }
    }
  });

  useEffect(() => {
    directionRef.current = direction === 'left' ? 1 : -1;
    elapsedRef.current = 0;
    progress.set(0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [direction]);

  // Transform: p=0 -> 150% (shine off right), p=100 -> -50% (shine off left)
  const backgroundPosition = useTransform(progress, p => `${150 - p * 2}% center`);

  const handleMouseEnter = useCallback(() => {
    if (pauseOnHover) setIsPaused(true);
  }, [pauseOnHover]);

  const handleMouseLeave = useCallback(() => {
    if (pauseOnHover) setIsPaused(false);
  }, [pauseOnHover]);

  const gradientStyle: React.CSSProperties = {
    backgroundImage: `linear-gradient(${spread}deg, ${color} 0%, ${color} 35%, ${shineColor} 50%, ${color} 65%, ${color} 100%)`,
    backgroundSize: '200% auto',
    WebkitBackgroundClip: 'text',
    backgroundClip: 'text',
    WebkitTextFillColor: 'transparent'
  };

  return (
    <motion.span
      className={`inline-block ${className}`}
      style={{ ...gradientStyle, backgroundPosition }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {text}
    </motion.span>
  );
};

export default ShinyText;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design

Create a React component called TextPressure that implements a "pressure-sensitive" typography effect. When the user moves their mouse over the text, the characters nearest to the cursor should visually "expand" and "weight up" using Variable Font technology.

# Key Requirements

1. Variable Font Usage:

   - You MUST use a variable font that supports wght (Weight), wdth (Width), and ital (Italic) axes.

   - Inject the @font-face dynamically or via a style tag.

2. Proximity Logic:

   - The component should track the mouse cursor position globally (window event) or locally.

   - For every character in the text string, calculate the Euclidean distance between the cursor and the center of that specific character bounding box.

   - Use requestAnimationFrame to ensure this calculation runs at 60fps without lag.

3. Interpolation (The "Pressure" Math):

   - Define a maxDistance (influence radius).

   - If the cursor is within maxDistance of a character:

     - Map the distance (0 to max) to the font variation axes.

     - Closer = Higher Weight (e.g., 900), Wider Width (e.g., 100), Higher Slant.

     - Further = Lower Weight (e.g., 100), Narrower Width (e.g., 50), No Slant.

   - Use CSS `font-variation-settings

   You are given a task to integrate an existing React component in the codebase

~~~/README.md
# Aurora

A high-performance WebGL aurora borealis effect using OGL. This component creates a smooth, flowing gradient animation that simulates the northern lights with configurable colors, speed, and intensity.

## Usage

```tsx
import { Aurora } from '@/sd-components/320ca513-9e1d-4da7-ad85-92f1717417a7';

function MyComponent() {
  return (
    <div style={{ height: '500px', width: '100%', position: 'relative' }}>
      <Aurora
        colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
        blend={0.5}
        amplitude={1.0}
        speed={0.5}
      />
    </div>
  );
}
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `colorStops` | `string[]` | `['#5227FF', '#7cff67', '#5227FF']` | Array of 3 hex color strings defining the gradient ramp. |
| `amplitude` | `number` | `1.0` | Controls the height/intensity of the aurora waves. |
| `blend` | `number` | `0.5` | Controls the softness/blend of the color edges. |
| `speed` | `number` | `1.0` | Multiplier for the animation speed. |
| `time` | `number` | `undefined` | Optional override for the time uniform (for manual control). |

## Dependencies

- `ogl`: Lightweight WebGL library
- `react`: Component framework
~~~

~~~/src/App.tsx
import { Aurora } from './Component';
import { RefreshCw, Play, RotateCcw } from 'lucide-react';
import { useState } from 'react';

export default function App() {
  const [key, setKey] = useState(0);

  const handleReplay = () => {
    setKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#1A1A1B] p-8 font-sans">
      <div className="w-full max-w-4xl relative">
        {/* Main Content Card */}
        <div className="relative overflow-hidden rounded-2xl bg-black/20 border border-white/5 shadow-[0_0_40px_rgba(0,0,0,0.2)] aspect-[16/9]">
          
          {/* Background Gradient to blend with Aurora */}
          <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-transparent to-black/40 z-10 pointer-events-none" />
          
          {/* Aurora Component */}
          <div className="absolute inset-0 z-0">
            <Aurora
              key={key}
              colorStops={["#3A29FF", "#FF94B4", "#FF3232"]}
              blend={0.5}
              amplitude={1.0}
              speed={0.5}
            />
          </div>

          {/* Foreground Content */}
          <div className="absolute inset-0 z-20 p-8 flex flex-col justify-between">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-3xl font-medium text-white tracking-tight mb-2">
                  Aurora Borealis
                </h1>
                <p className="text-white/60 text-sm max-w-xs leading-relaxed">
                  A WebGL-based fluid simulation mimicking the northern lights using OGL.
                </p>
              </div>
              <div className="flex gap-2">
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-white/10 text-white/80 border border-white/5 backdrop-blur-sm">
                  WebGL
                </span>
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-white/10 text-white/80 border border-white/5 backdrop-blur-sm">
                  OGL
                </span>
              </div>
            </div>

            {/* Controls / Footer */}
            <div className="flex items-center justify-between mt-auto">
              <div className="flex items-center gap-4">
                 <button 
                  onClick={handleReplay}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm font-medium transition-colors backdrop-blur-md border border-white/10 group"
                >
                  <RotateCcw className="w-4 h-4 text-white/80 group-hover:-rotate-180 transition-transform duration-500" />
                  <span>Replay</span>
                </button>
              </div>
              
              <div className="text-right">
                <div className="text-white/40 text-xs font-mono">
                  AMPLITUDE: 1.0 <br/> SPEED: 0.5
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative elements outside */}
        <div className="absolute -top-12 -left-12 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none mix-blend-screen" />
        <div className="absolute -bottom-12 -right-12 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none mix-blend-screen" />
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "aurora-component",
  "description": "A WebGL-based aurora borealis effect using OGL",
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "ogl": "^1.0.11",
    "lucide-react": "^0.344.0"
  }
}
~~~

~~~/src/Component.tsx
import { useEffect, useRef } from 'react';
import { Renderer, Program, Mesh, Color, Triangle } from 'ogl';

const VERT = `#version 300 es
in vec2 position;
void main() {
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const FRAG = `#version 300 es
precision highp float;

uniform float uTime;
uniform float uAmplitude;
uniform vec3 uColorStops[3];
uniform vec2 uResolution;
uniform float uBlend;

out vec4 fragColor;

vec3 permute(vec3 x) {
  return mod(((x * 34.0) + 1.0) * x, 289.0);
}

float snoise(vec2 v){
  const vec4 C = vec4(
      0.211324865405187, 0.366025403784439,
      -0.577350269189626, 0.024390243902439
  );
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute(
      permute(i.y + vec3(0.0, i1.y, 1.0))
    + i.x + vec3(0.0, i1.x, 1.0)
  );
  vec3 m = max(
      0.5 - vec3(
          dot(x0, x0),
          dot(x12.xy, x12.xy),
          dot(x12.zw, x12.zw)
      ), 
      0.0
  );
  m = m * m;
  m = m * m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m = 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}

struct ColorStop {
  vec3 color;
  float position;
};

#define COLOR_RAMP(colors, factor, finalColor) {              \
  int index = 0;                                            \
  for (int i = 0; i < 2; i++) {                               \
     ColorStop currentColor = colors[i];                    \
     bool isInBetween = currentColor.position <= factor;    \
     index = int(mix(float(index), float(i), float(isInBetween))); \
  }                                                         \
  ColorStop currentColor = colors[index];                   \
  ColorStop nextColor = colors[index + 1];                  \
  float range = nextColor.position - currentColor.position; \
  float lerpFactor = (factor - currentColor.position) / range; \
  finalColor = mix(currentColor.color, nextColor.color, lerpFactor); \
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  
  ColorStop colors[3];
  colors[0] = ColorStop(uColorStops[0], 0.0);
  colors[1] = ColorStop(uColorStops[1], 0.5);
  colors[2] = ColorStop(uColorStops[2], 1.0);
  
  vec3 rampColor;
  COLOR_RAMP(colors, uv.x, rampColor);
  
  float height = snoise(vec2(uv.x * 2.0 + uTime * 0.1, uTime * 0.25)) * 0.5 * uAmplitude;
  height = exp(height);
  height = (uv.y * 2.0 - height + 0.2);
  float intensity = 0.6 * height;
  
  float midPoint = 0.20;
  float auroraAlpha = smoothstep(midPoint - uBlend * 0.5, midPoint + uBlend * 0.5, intensity);
  
  vec3 auroraColor = intensity * rampColor;
  
  fragColor = vec4(auroraColor * auroraAlpha, auroraAlpha);
}
`;

export interface AuroraProps {
  colorStops?: string[];
  amplitude?: number;
  blend?: number;
  time?: number;
  speed?: number;
}

export function Aurora(props: AuroraProps) {
  const { colorStops = ['#5227FF', '#7cff67', '#5227FF'], amplitude = 1.0, blend = 0.5 } = props;
  const propsRef = useRef<AuroraProps>(props);
  propsRef.current = props;

  const ctnDom = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctn = ctnDom.current;
    if (!ctn) return;

    const renderer = new Renderer({
      alpha: true,
      premultipliedAlpha: true,
      antialias: true
    });
    const gl = renderer.gl;
    
    gl.clearColor(0, 0, 0, 0);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    
    // Ensure canvas is transparent
    gl.canvas.style.backgroundColor = 'transparent';

    let program: Program | undefined;

    function resize() {
      if (!ctn) return;
      const width = ctn.offsetWidth;
      const height = ctn.offsetHeight;
      renderer.setSize(width, height);
      if (program) {
        program.uniforms.uResolution.value = [width, height];
      }
    }
    window.addEventListener('resize', resize);

    const geometry = new Triangle(gl);
    if (geometry.attributes.uv) {
      delete geometry.attributes.uv;
    }

    const colorStopsArray = colorStops.map(hex => {
      const c = new Color(hex);
      return [c.r, c.g, c.b];
    });

    program = new Program(gl, {
      vertex: VERT,
      fragment: FRAG,
      uniforms: {
        uTime: { value: 0 },
        uAmplitude: { value: amplitude },
        uColorStops: { value: colorStopsArray },
        uResolution: { value: [ctn.offsetWidth, ctn.offsetHeight] },
        uBlend: { value: blend }
      }
    });

    const mesh = new Mesh(gl, { geometry, program });
    ctn.appendChild(gl.canvas);

    let animateId = 0;
    const update = (t: number) => {
      animateId = requestAnimationFrame(update);
      const { time = t * 0.01, speed = 1.0 } = propsRef.current;
      
      if (program) {
        program.uniforms.uTime.value = time * speed * 0.1;
        program.uniforms.uAmplitude.value = propsRef.current.amplitude ?? 1.0;
        program.uniforms.uBlend.value = propsRef.current.blend ?? blend;
        
        const stops = propsRef.current.colorStops ?? colorStops;
        program.uniforms.uColorStops.value = stops.map((hex: string) => {
          const c = new Color(hex);
          return [c.r, c.g, c.b];
        });
        
        renderer.render({ scene: mesh });
      }
    };
    animateId = requestAnimationFrame(update);
    resize();

    return () => {
      cancelAnimationFrame(animateId);
      window.removeEventListener('resize', resize);
      if (ctn && gl.canvas.parentNode === ctn) {
        ctn.removeChild(gl.canvas);
      }
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    };
  }, [amplitude]);

  return <div ref={ctnDom} className="w-full h-full" />;
}

export default Aurora;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design


### **The "Exploded View" Assembly**

Perfect for showing product components or "how it works."

> *"Pin a central product mockup. As the user scrolls, have the internal components (UI elements, icons, layers) 'explode' outwards in different directions. As they continue to scroll, have the components fly back together and 'lock' into a final, different layout."*


### **The "Lens Flare" or "Spotlight" Mask**

A high-end "Dark Mode" interaction.

> *"Cover the section with a solid black overlay. Create a circular clip-path mask that is tied to the scroll progress. As the user moves down the page, the 'spotlight' mask should grow from 0% to 150% in size, revealing the colorful UI layout hidden beneath the black layer."*


The "Parallax Tilt" Grid 

Makes a standard 3-column grid feel alive.

"In a 3-column image grid, apply independent scroll speeds to each column (e.g., left: 1.2x, center: 1.0x, right: 1.4x). Additionally, add a scroll-linked 3D tilt where the images lean forward as they enter from the bottom and lean back as they exit the top."


Create a typing animation that reveals each character with a 50ms delay between characters for the main headline.

The "Stacking Cards" Effect:

> *"As the user scrolls through the [Portfolio], have each card stay sticky at the top, so the next card appears to slide over the previous one like a deck of cards."*


Sticky Content Switch:

> *"Pin the left-side heading in place while the right-side images scroll past. As each new image reaches the center, update the heading text to match the image content."*


Full-Screen Image Expansion:

> *Start with a featured image centered in a small frame. As the user scrolls, have the image expand smoothly until it fills the entire width and height of the browser.*

Add a hand-drawn underline animation to the keyword [Target Word] that triggers when the user scrolls it into view.


Animate an SVG line (like a connector or 'journey' line) that draws itself forward based on the user's scroll percentage.

Animate the headline by having each word slide up from behind an invisible mask. The movement should be fast at the start and slow down at the end (Power4.out ease), creating a premium, cinematic feel.

Create a text component that animates words changing like a physical slot machine or Rolodex. 

**Animation**: The old word should rotate 90° backward on the X-axis, while the new word flips up from the bottom. 

**Layout & Alignment**: This will be used inline (e.g., "We Deliver [Word]"). **CRITICAL**: Left-align the text within its container so it stays flush against the preceding text. 

Do not center it, or variable word lengths will create awkward gaps. 

**Technical**: Ensure the container uses preserve-3d and isn't strictly clipped, so the 3D rotation is fully visible.


Create a 'sticky' section where the vertical scroll locks, and the content slides horizontally to showcase a gallery. 

**Technical Requirement**: Ensure the GSAP initialization is robust. Since this is a React component, please include a small delay or safety check inside useLayoutEffect to ensure the DOM is fully rendered and widths are accurate before the ScrollTrigger calculates the pinning logic.


Fade in the heading character by character, with each letter starting at 50% opacity and moving from a 5px blur to sharp focus. Stagger the delay by 0.02s per character.

As the user scrolls, gradually change the font-weight of the text from Light (300) to Extra Bold (800) based on their scroll progress through the section.

Make the keyword subtly glow by animating a text-shadow from 'none' to a soft [Color] bloom, pulsing gently like a breathing rhythm.

Apply a subtle SVG displacement map to the text to give it a 'liquid' or 'wavy' appearance that undulates gently, as if the letters are underwater.

As the text scrolls over a dark image or a different colored section, use a 'mix-blend-mode: difference' effect so the text color automatically flips to stay legible.


Add a vertical text clip slide-down animation letter by letter.

Numbers are displayed in large font with a **count-up animation**, triggering a **dynamic increase effect when scrolling into the viewport**—suitable for data display sections or statistical information areas.


H3 heading component styled with Tailwind CSS.Includes responsive font sizing, tight letter tracking, and smooth color transitions—ideal for hero banners, section headers.

Create a complex **animation that fades in, slides up, and reduces blur for each letter**.


Responsive oversized heading with **fade text effect**,

Features fluid typography that scales with viewport size.Create a text animation that **slides in with a clipping mask effect.**

Help me implement this scroll animation component, as i scroll one of shape center, become bigger and connect to all other smaller shapes


Create a horizontal scroll animation using GSAP ScrollTrigger. \
\
Layout: Instead of full-screen slides, I want a continuous horizontal text flow - imagine a single, very long sentenceStructure: Use a single flex container so items flow naturally next to each other with variable gaps. \
\
Content: The sentence is 'In every bottle, discover the undeniable Real Magic of sharing pure Refreshment that brings us Together'. \
\
Integration: Embed the visual elements (SVG curves, icons) inline with the text, acting like punctuation or conjunctions, rather than separating them into their own distinct sections. \
\
Vibe: It should feel like reading a really long ticker tape, not flipping through a slide deck


I want to create a personal portfolio landing page for \[YOUR NAME\]. The page should be a full-screen hero section with a large headshot image \[IMAGE ONE\] as the background, centered and covering the entire viewport. My name should appear in the top left corner in a large, elegant serif font (like Playfair Display) with the first and last name stacked on separate lines. In the top right corner, add a "Portfolio" link. At the bottom right, include social media icons for Instagram, X/Twitter, YouTube, and LinkedIn that link to my profiles - use solid filled SVG icons so they're clearly visible.\
\
The main interactive feature should be a blob cursor effect that follows the mouse. When the user hovers over the page, an organic, gooey blob shape should appear and follow the cursor with a slight lag for a smooth, fluid feel. This blob should act as a "reveal" mask that shows a second version of the headshot \[IMAGE TWO\] - so as the user moves their cursor around, they're essentially revealing an alternate image underneath. The blob should have a trailing effect where smaller, fading blob shapes follow behind based on cursor speed - faster movement creates more pronounced trails. Add subtle animated wave lines in the background that respond gently to mouse movement.\
\
All text elements (my name, the Portfolio link, and the social icons) should dynamically invert to white when the blob cursor hovers over them, so they remain visible against the revealed image. The transitions should be smooth with a 300ms duration. Add a subtle parallax effect where elements shift slightly in the opposite direction of cursor movement to create depth. The overall aesthetic should be minimal and sophisticated with a white background, letting the photography and interactive elements be the focal point.
