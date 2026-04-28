You are given a task to integrate an existing React component in the codebase

~~~/README.md
# GridDistortionBackground

A high-performance WebGL-based grid distortion effect for background images, featuring interactive mouse-driven liquid-like ripples.

## Dependencies

- `react`: ^18.2.0
- `three`: ^0.160.0
- `lucide-react`: ^0.344.0

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `imageSrc` | `string` | **Required** | Source URL for the background image |
| `grid` | `number` | `15` | Number of grid cells (density) |
| `mouse` | `number` | `0.1` | Radius of mouse influence (0 to 1) |
| `strength` | `number` | `0.15` | Strength of the distortion effect |
| `relaxation` | `number` | `0.9` | How quickly the grid returns to normal (0 to 1) |
| `className` | `string` | `""` | Optional CSS class for the container |

## Usage

```tsx
import { GridDistortion } from '@/sd-components/7a22cbc7-e820-4de2-8730-fe82e9e587bb';

function MyPage() {
  return (
    <div style={{ width: '100%', height: '600px' }}>
      <GridDistortion
        imageSrc="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05"
        grid={20}
        mouse={0.2}
        strength={0.15}
        relaxation={0.95}
      />
    </div>
  );
}
```
~~~

~~~/src/App.tsx
/**
 * Demo application for GridDistortionBackground
 */

import React from 'react';
import { GridDistortion } from './Component';
import { RefreshCcw } from 'lucide-react';

export default function App() {
  const [key, setKey] = React.useState(0);

  return (
    <div className="min-h-screen bg-background flex flex-center p-20">
      <div className="w-full max-w-5xl aspect-video relative rounded-3xl overflow-hidden shadow-[0_40px_80px_-20px_rgba(0,0,0,0.05)] border-none">
        <GridDistortion
          key={key}
          imageSrc="https://picsum.photos/1920/1080?grayscale&random=1"
          grid={20}
          mouse={0.15}
          strength={0.2}
          relaxation={0.96}
        />
        
        {/* Floating Label as per Project System Prompt */}
        <div className="absolute top-8 left-8 z-10">
          <h1 className="text-xl font-medium text-foreground/80 tracking-tight">
            Grid Distortion
          </h1>
        </div>

        {/* Reply/Reset Button as per Project System Prompt */}
        <button 
          onClick={() => setKey(prev => prev + 1)}
          className="absolute bottom-8 right-8 z-10 w-12 h-12 flex items-center justify-center bg-background/80 backdrop-blur-md rounded-full border border-border/50 text-foreground/60 hover:text-primary transition-all active:scale-95 shadow-sm"
          title="Refresh Effect"
        >
          <RefreshCcw className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "grid-distortion-background",
  "description": "A high-performance WebGL-based grid distortion effect for background images.",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "three": "^0.160.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.344.0"
  }
}
~~~

~~~/src/Component.tsx
/**
 * GridDistortionBackground Component
 * 
 * A high-performance WebGL-based grid distortion effect.
 * Uses Three.js for rendering and a custom fragment shader to achieve
 * liquid-like ripples when the mouse interacts with the image.
 */

import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

export interface GridDistortionProps {
  /** Number of grid cells (density) */
  grid?: number;
  /** Radius of mouse influence (0 to 1) */
  mouse?: number;
  /** Strength of the distortion effect */
  strength?: number;
  /** How quickly the grid returns to normal (0 to 1) */
  relaxation?: number;
  /** Source URL for the background image */
  imageSrc: string;
  /** Optional CSS class for the container */
  className?: string;
}

const vertexShader = `
uniform float time;
varying vec2 vUv;
varying vec3 vPosition;
void main() {
  vUv = uv;
  vPosition = position;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const fragmentShader = `
uniform sampler2D uDataTexture;
uniform sampler2D uTexture;
uniform vec4 resolution;
varying vec2 vUv;
void main() {
  vec2 uv = vUv;
  vec4 offset = texture2D(uDataTexture, vUv);
  gl_FragColor = texture2D(uTexture, uv - 0.02 * offset.rg);
}
`;

export function GridDistortion({
  grid = 15,
  mouse = 0.1,
  strength = 0.15,
  relaxation = 0.9,
  imageSrc,
  className = ''
}: GridDistortionProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.OrthographicCamera | null>(null);
  const planeRef = useRef<THREE.Mesh | null>(null);
  const animationIdRef = useRef<number | null>(null);
  const resizeObserverRef = useRef<ResizeObserver | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    rendererRef.current = renderer;
    
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    const camera = new THREE.OrthographicCamera(0, 0, 0, 0, -1000, 1000);
    camera.position.z = 2;
    cameraRef.current = camera;

    const uniforms = {
      time: { value: 0 },
      resolution: { value: new THREE.Vector4() },
      uTexture: { value: null as THREE.Texture | null },
      uDataTexture: { value: null as THREE.DataTexture | null }
    };

    const textureLoader = new THREE.TextureLoader();
    textureLoader.load(imageSrc, texture => {
      texture.minFilter = THREE.LinearFilter;
      texture.magFilter = THREE.LinearFilter;
      texture.wrapS = THREE.ClampToEdgeWrapping;
      texture.wrapT = THREE.ClampToEdgeWrapping;
      uniforms.uTexture.value = texture;
      handleResize();
    });

    const size = grid;
    const data = new Float32Array(4 * size * size);
    for (let i = 0; i < size * size; i++) {
      data[i * 4] = 0;
      data[i * 4 + 1] = 0;
    }

    const dataTexture = new THREE.DataTexture(data, size, size, THREE.RGBAFormat, THREE.FloatType);
    dataTexture.needsUpdate = true;
    uniforms.uDataTexture.value = dataTexture;

    const material = new THREE.ShaderMaterial({
      side: THREE.DoubleSide,
      uniforms,
      vertexShader,
      fragmentShader,
      transparent: true
    });

    const geometry = new THREE.PlaneGeometry(1, 1, size - 1, size - 1);
    const plane = new THREE.Mesh(geometry, material);
    planeRef.current = plane;
    scene.add(plane);

    const handleResize = () => {
      if (!container || !renderer || !camera) return;
      const rect = container.getBoundingClientRect();
      const width = rect.width;
      const height = rect.height;
      if (width === 0 || height === 0) return;

      const containerAspect = width / height;
      renderer.setSize(width, height);

      if (plane) {
        plane.scale.set(containerAspect, 1, 1);
      }

      const frustumHeight = 1;
      const frustumWidth = frustumHeight * containerAspect;
      camera.left = -frustumWidth / 2;
      camera.right = frustumWidth / 2;
      camera.top = frustumHeight / 2;
      camera.bottom = -frustumHeight / 2;
      camera.updateProjectionMatrix();
      uniforms.resolution.value.set(width, height, 1, 1);
    };

    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver(() => {
        handleResize();
      });
      resizeObserver.observe(container);
      resizeObserverRef.current = resizeObserver;
    } else {
      window.addEventListener('resize', handleResize);
    }

    const mouseState = {
      x: 0,
      y: 0,
      prevX: 0,
      prevY: 0,
      vX: 0,
      vY: 0
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = 1 - (e.clientY - rect.top) / rect.height;
      
      mouseState.vX = x - mouseState.prevX;
      mouseState.vY = y - mouseState.prevY;
      
      mouseState.x = x;
      mouseState.y = y;
      mouseState.prevX = x;
      mouseState.prevY = y;
    };

    const handleMouseLeave = () => {
      mouseState.x = 0;
      mouseState.y = 0;
      mouseState.prevX = 0;
      mouseState.prevY = 0;
      mouseState.vX = 0;
      mouseState.vY = 0;
    };

    container.addEventListener('mousemove', handleMouseMove);
    container.addEventListener('mouseleave', handleMouseLeave);

    handleResize();

    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);
      if (!renderer || !scene || !camera || !dataTexture) return;

      uniforms.time.value += 0.05;

      const dataArr = dataTexture.image.data as Float32Array;
      
      // Decay existing distortion
      for (let i = 0; i < size * size; i++) {
        dataArr[i * 4] *= relaxation;
        dataArr[i * 4 + 1] *= relaxation;
      }

      // Add new distortion from mouse
      const gridMouseX = size * mouseState.x;
      const gridMouseY = size * mouseState.y;
      const maxDist = size * mouse;

      for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
          const dx = gridMouseX - i;
          const dy = gridMouseY - j;
          const distSq = dx * dx + dy * dy;
          
          if (distSq < maxDist * maxDist) {
            const index = 4 * (i + size * j);
            const dist = Math.sqrt(distSq);
            const power = Math.max(0, 1 - dist / maxDist);
            
            dataArr[index] += strength * mouseState.vX * power * 10;
            dataArr[index + 1] -= strength * mouseState.vY * power * 10;
          }
        }
      }

      dataTexture.needsUpdate = true;
      renderer.render(scene, camera);
    };

    animate();

    return () => {
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
      if (resizeObserverRef.current) {
        resizeObserverRef.current.disconnect();
      } else {
        window.removeEventListener('resize', handleResize);
      }
      container.removeEventListener('mousemove', handleMouseMove);
      container.removeEventListener('mouseleave', handleMouseLeave);
      
      if (renderer) {
        renderer.dispose();
        if (container.contains(renderer.domElement)) {
          container.removeChild(renderer.domElement);
        }
      }
      if (planeRef.current) {
        planeRef.current.geometry.dispose();
        (planeRef.current.material as THREE.Material).dispose();
      }
      if (dataTexture) dataTexture.dispose();
      if (uniforms.uTexture.value) uniforms.uTexture.value.dispose();
      
      sceneRef.current = null;
      rendererRef.current = null;
      cameraRef.current = null;
      planeRef.current = null;
    };
  }, [grid, mouse, strength, relaxation, imageSrc]);

  return (
    <div
      ref={containerRef}
      className={`relative overflow-hidden ${className}`}
      style={{
        width: '100%',
        height: '100%',
        minWidth: '0',
        minHeight: '0'
      }}
    />
  );
}

export default GridDistortion;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
