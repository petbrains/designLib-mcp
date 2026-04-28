You are given a task to integrate an existing React component in the codebase

~~~/README.md
# FlyingPosters

A high-performance WebGL-powered 3D vertical gallery with smooth scroll distortion. Powered by OGL for lightweight and efficient rendering.

## Features
- **3D Distortion**: Planes warp and rotate based on scroll velocity and position.
- **Infinite Scroll**: Seamless looping gallery mechanism.
- **GPU Accelerated**: Minimal CPU overhead using OGL.
- **Interactive**: Supports wheel, touch, and mouse drag navigation.

## Dependencies
- `ogl`: ^0.0.116

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `string[]` | `[]` | Array of image URLs to display in the gallery |
| `planeWidth` | `number` | `320` | Width of each poster in the WebGL world |
| `planeHeight` | `number` | `440` | Height of each poster in the WebGL world |
| `distortion` | `number` | `3` | Intensity of the warping effect during scroll |
| `scrollEase` | `number` | `0.05` | Smoothing factor for the scrolling motion |
| `cameraFov` | `number` | `45` | Field of view for the perspective camera |
| `cameraZ` | `number` | `20` | Camera distance from the scene origin |

## Usage

```tsx
import { FlyingPosters } from '@/sd-components/71be5e84-8b21-4928-a45c-e533672eb5e2';

export default function MyGallery() {
  const images = [
    'https://example.com/image1.jpg',
    'https://example.com/image2.jpg',
    'https://example.com/image3.jpg',
  ];

  return (
    <div style={{ height: '800px', width: '100%' }}>
      <FlyingPosters 
        items={images}
        distortion={4}
        scrollEase={0.06}
      />
    </div>
  );
}
```
~~~

~~~/src/App.tsx
import React from 'react';
import { FlyingPosters } from './Component';

/**
 * App component showcasing the FlyingPosters gallery.
 * Following the 'Minimalist Showcase' style guide:
 * - Clean deep slate background
 * - Ample whitespace
 * - Title focused on the animation name
 * - Reply button included
 */
export default function App() {
  const images = [
    'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550684399-3f41d5d1942d?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550684376-efcbd6e3f031?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550684847-75bdda21cc95?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550684400-9dd93645b274?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1550684399-3f41d5d1942d?q=80&w=800&auto=format&fit=crop',
  ];

  return (
    <div className="min-h-screen bg-[#1A1A1B] flex flex-col items-center justify-center p-20 font-sans">
      <div className="w-full max-w-4xl aspect-[4/5] relative rounded-3xl overflow-hidden shadow-[0_40px_100px_rgba(0,0,0,0.5)] border border-white/5">
        <FlyingPosters 
          items={images}
          planeWidth={400}
          planeHeight={540}
          distortion={4}
          scrollEase={0.06}
        />
        
        {/* Floating Title Overlay */}
        <div className="absolute top-12 left-12 z-10">
          <h1 className="text-white text-2xl font-medium tracking-tight opacity-90">
            Flying Posters
          </h1>
          <p className="text-white/40 text-sm mt-2 font-normal">
            WebGL 3D Distortion Gallery
          </p>
        </div>

        {/* Scroll Hint */}
        <div className="absolute bottom-12 right-12 z-10 flex flex-col items-end">
          <span className="text-white/30 text-xs uppercase tracking-[0.2em] mb-2">Scroll to explore</span>
          <div className="w-px h-12 bg-gradient-to-b from-white/40 to-transparent" />
        </div>

        {/* Reply Button - Required by system prompt */}
        <button 
          className="absolute bottom-12 left-12 z-10 bg-white/10 hover:bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-full text-sm font-medium transition-all border border-white/10 flex items-center gap-2"
          onClick={() => window.location.reload()}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
            <path d="M3 3v5h5" />
          </svg>
          Replay
        </button>
      </div>
    </div>
  );
}
~~~

~~~/package.json
{
  "name": "flying-posters-showcase",
  "description": "WebGL-powered 3D vertical gallery with scroll distortion",
  "dependencies": {
    "ogl": "^0.0.116",
    "lucide-react": "latest",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.2"
  }
}
~~~

~~~/src/Component.tsx
/**
 * FlyingPosters Component
 * A WebGL-powered 3D vertical scroll gallery using OGL.
 * Features:
 * - 3D plane distortion based on scroll position
 * - Infinite looping scroll mechanism
 * - Responsive canvas resizing
 * - Smooth lerped motion
 */

import React, { useRef, useEffect } from 'react';
import { Renderer, Camera, Transform, Plane, Program, Mesh, Texture, type OGLRenderingContext } from 'ogl';

type GL = OGLRenderingContext;
type OGLProgram = Program;
type OGLMesh = Mesh;
type OGLTransform = Transform;
type OGLPlane = Plane;

interface ScreenSize {
  width: number;
  height: number;
}

interface ViewportSize {
  width: number;
  height: number;
}

interface ScrollState {
  position?: number;
  ease: number;
  current: number;
  target: number;
  last: number;
}

interface AutoBindOptions {
  include?: Array<string | RegExp>;
  exclude?: Array<string | RegExp>;
}

interface MediaParams {
  gl: GL;
  geometry: OGLPlane;
  scene: OGLTransform;
  screen: ScreenSize;
  viewport: ViewportSize;
  image: string;
  length: number;
  index: number;
  planeWidth: number;
  planeHeight: number;
  distortion: number;
}

interface CanvasParams {
  container: HTMLElement;
  canvas: HTMLCanvasElement;
  items: string[];
  planeWidth: number;
  planeHeight: number;
  distortion: number;
  scrollEase: number;
  cameraFov: number;
  cameraZ: number;
}

const vertexShader = `
precision highp float;
attribute vec3 position;
attribute vec2 uv;
attribute vec3 normal;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
uniform mat3 normalMatrix;

uniform float uPosition;
uniform float uTime;
uniform float uSpeed;
uniform vec3 distortionAxis;
uniform vec3 rotationAxis;
uniform float uDistortion;

varying vec2 vUv;
varying vec3 vNormal;

float PI = 3.141592653589793238;

mat4 rotationMatrix(vec3 axis, float angle) {
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    
    return mat4(
      oc * axis.x * axis.x + c,         oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
      oc * axis.x * axis.y + axis.z * s,oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
      oc * axis.z * axis.x - axis.y * s,oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
      0.0,                              0.0,                                0.0,                                1.0
    );
}

vec3 rotate(vec3 v, vec3 axis, float angle) {
  mat4 m = rotationMatrix(axis, angle);
  return (m * vec4(v, 1.0)).xyz;
}

float qinticInOut(float t) {
  return t < 0.5
    ? 16.0 * pow(t, 5.0)
    : -0.5 * abs(pow(2.0 * t - 2.0, 5.0)) + 1.0;
}

void main() {
  vUv = uv;
  
  float norm = 0.5;
  vec3 newpos = position;
  float offset = (dot(distortionAxis, position) + norm / 2.) / norm;
  float localprogress = clamp(
    (fract(uPosition * 5.0 * 0.01) - 0.01 * uDistortion * offset) / (1. - 0.01 * uDistortion),
    0.,
    2.
  );
  localprogress = qinticInOut(localprogress) * PI;
  newpos = rotate(newpos, rotationAxis, localprogress);
  gl_Position = projectionMatrix * modelViewMatrix * vec4(newpos, 1.0);
}
`;

const fragmentShader = `
precision highp float;
uniform vec2 uImageSize;
uniform vec2 uPlaneSize;
uniform sampler2D tMap;
varying vec2 vUv;

void main() {
  vec2 imageSize = uImageSize;
  vec2 planeSize = uPlaneSize;
  float imageAspect = imageSize.x / imageSize.y;
  float planeAspect = planeSize.x / planeSize.y;
  vec2 scale = vec2(1.0, 1.0);
  if (planeAspect > imageAspect) {
      scale.x = imageAspect / planeAspect;
  } else {
      scale.y = planeAspect / imageAspect;
  }
  vec2 uv = vUv * scale + (1.0 - scale) * 0.5;
  gl_FragColor = texture2D(tMap, uv);
}
`;

function AutoBind(self: any, { include, exclude }: AutoBindOptions = {}) {
  const getAllProperties = (object: any): Set<[any, string | symbol]> => {
    const properties = new Set<[any, string | symbol]>();
    do {
      for (const key of Reflect.ownKeys(object)) {
        properties.add([object, key]);
      }
    } while ((object = Reflect.getPrototypeOf(object)) && object !== Object.prototype);
    return properties;
  };

  const filter = (key: string | symbol) => {
    const match = (pattern: string | RegExp) =>
      typeof pattern === 'string' ? key === pattern : (pattern as RegExp).test(key.toString());
    if (include) return include.some(match);
    if (exclude) return !exclude.some(match);
    return true;
  };

  for (const [object, key] of getAllProperties(self.constructor.prototype)) {
    if (key === 'constructor' || !filter(key)) continue;
    const descriptor = Reflect.getOwnPropertyDescriptor(object, key);
    if (descriptor && typeof descriptor.value === 'function') {
      self[key] = self[key].bind(self);
    }
  }
  return self;
}

function lerp(p1: number, p2: number, t: number): number {
  return p1 + (p2 - p1) * t;
}

function map(num: number, min1: number, max1: number, min2: number, max2: number, round = false): number {
  const num1 = (num - min1) / (max1 - min1);
  const num2 = num1 * (max2 - min2) + min2;
  return round ? Math.round(num2) : num2;
}

class Media {
  gl: GL;
  geometry: OGLPlane;
  scene: OGLTransform;
  screen: ScreenSize;
  viewport: ViewportSize;
  image: string;
  length: number;
  index: number;
  planeWidth: number;
  planeHeight: number;
  distortion: number;
  program!: OGLProgram;
  plane!: OGLMesh;
  extra = 0;
  padding = 0;
  height = 0;
  heightTotal = 0;
  y = 0;

  constructor({
    gl,
    geometry,
    scene,
    screen,
    viewport,
    image,
    length,
    index,
    planeWidth,
    planeHeight,
    distortion
  }: MediaParams) {
    this.gl = gl;
    this.geometry = geometry;
    this.scene = scene;
    this.screen = screen;
    this.viewport = viewport;
    this.image = image;
    this.length = length;
    this.index = index;
    this.planeWidth = planeWidth;
    this.planeHeight = planeHeight;
    this.distortion = distortion;
    this.createShader();
    this.createMesh();
    this.onResize();
  }

  createShader() {
    const texture = new Texture(this.gl, { generateMipmaps: false });
    this.program = new Program(this.gl, {
      depthTest: false,
      depthWrite: false,
      fragment: fragmentShader,
      vertex: vertexShader,
      uniforms: {
        tMap: { value: texture },
        uPosition: { value: 0 },
        uPlaneSize: { value: [0, 0] },
        uImageSize: { value: [0, 0] },
        uSpeed: { value: 0 },
        rotationAxis: { value: [0, 1, 0] },
        distortionAxis: { value: [1, 1, 0] },
        uDistortion: { value: this.distortion },
        uViewportSize: { value: [this.viewport.width, this.viewport.height] },
        uTime: { value: 0 }
      },
      cullFace: false
    });

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = this.image;
    img.onload = () => {
      texture.image = img;
      this.program.uniforms.uImageSize.value = [img.naturalWidth, img.naturalHeight];
    };
  }

  createMesh() {
    this.plane = new Mesh(this.gl, {
      geometry: this.geometry,
      program: this.program
    });
    this.plane.setParent(this.scene);
  }

  setScale() {
    this.plane.scale.x = (this.viewport.width * this.planeWidth) / this.screen.width;
    this.plane.scale.y = (this.viewport.height * this.planeHeight) / this.screen.height;
    this.plane.position.x = 0;
    this.program.uniforms.uPlaneSize.value = [this.plane.scale.x, this.plane.scale.y];
  }

  onResize({ screen, viewport }: { screen?: ScreenSize; viewport?: ViewportSize } = {}) {
    if (screen) this.screen = screen;
    if (viewport) {
      this.viewport = viewport;
      this.program.uniforms.uViewportSize.value = [viewport.width, viewport.height];
    }
    this.setScale();
    this.padding = 5;
    this.height = this.plane.scale.y + this.padding;
    this.heightTotal = this.height * this.length;
    this.y = -this.heightTotal / 2 + (this.index + 0.5) * this.height;
  }

  update(scroll: ScrollState) {
    this.plane.position.y = this.y - scroll.current - this.extra;
    const position = map(this.plane.position.y, -this.viewport.height, this.viewport.height, 5, 15);
    this.program.uniforms.uPosition.value = position;
    this.program.uniforms.uTime.value += 0.04;
    this.program.uniforms.uSpeed.value = scroll.current;

    const planeHeight = this.plane.scale.y;
    const viewportHeight = this.viewport.height;
    const topEdge = this.plane.position.y + planeHeight / 2;
    const bottomEdge = this.plane.position.y - planeHeight / 2;

    if (topEdge < -viewportHeight / 2) {
      this.extra -= this.heightTotal;
    } else if (bottomEdge > viewportHeight / 2) {
      this.extra += this.heightTotal;
    }
  }
}

class Canvas {
  container: HTMLElement;
  canvas: HTMLCanvasElement;
  items: string[];
  planeWidth: number;
  planeHeight: number;
  distortion: number;
  scroll: ScrollState;
  cameraFov: number;
  cameraZ: number;
  renderer!: Renderer;
  gl!: GL;
  camera!: Camera;
  scene!: OGLTransform;
  planeGeometry!: OGLPlane;
  medias!: Media[];
  screen!: ScreenSize;
  viewport!: ViewportSize;
  isDown = false;
  start = 0;
  loaded = 0;
  rafId: number = 0;

  constructor({
    container,
    canvas,
    items,
    planeWidth,
    planeHeight,
    distortion,
    scrollEase,
    cameraFov,
    cameraZ
  }: CanvasParams) {
    this.container = container;
    this.canvas = canvas;
    this.items = items;
    this.planeWidth = planeWidth;
    this.planeHeight = planeHeight;
    this.distortion = distortion;
    this.scroll = {
      ease: scrollEase,
      current: 0,
      target: 0,
      last: 0
    };
    this.cameraFov = cameraFov;
    this.cameraZ = cameraZ;

    AutoBind(this);

    this.createRenderer();
    this.createCamera();
    this.createScene();
    this.onResize();
    this.createGeometry();
    this.createMedias();
    this.update();
    this.addEventListeners();
    this.createPreloader();
  }

  createRenderer() {
    this.renderer = new Renderer({
      canvas: this.canvas,
      alpha: true,
      antialias: true,
      dpr: Math.min(window.devicePixelRatio, 2)
    });
    this.gl = this.renderer.gl;
  }

  createCamera() {
    this.camera = new Camera(this.gl);
    this.camera.fov = this.cameraFov;
    this.camera.position.z = this.cameraZ;
  }

  createScene() {
    this.scene = new Transform();
  }

  createGeometry() {
    this.planeGeometry = new Plane(this.gl, {
      heightSegments: 1,
      widthSegments: 100
    });
  }

  createMedias() {
    this.medias = this.items.map(
      (image, index) =>
        new Media({
          gl: this.gl,
          geometry: this.planeGeometry,
          scene: this.scene,
          screen: this.screen,
          viewport: this.viewport,
          image,
          length: this.items.length,
          index,
          planeWidth: this.planeWidth,
          planeHeight: this.planeHeight,
          distortion: this.distortion
        })
    );
  }

  createPreloader() {
    this.loaded = 0;
    this.items.forEach(src => {
      const image = new Image();
      image.crossOrigin = 'anonymous';
      image.src = src;
      image.onload = () => {
        if (++this.loaded === this.items.length) {
          // Preload complete
        }
      };
    });
  }

  onResize() {
    if (!this.container) return;
    const rect = this.container.getBoundingClientRect();
    this.screen = { width: rect.width, height: rect.height };
    this.renderer.setSize(this.screen.width, this.screen.height);
    this.camera.perspective({
      aspect: this.gl.canvas.width / this.gl.canvas.height
    });

    const fov = (this.camera.fov * Math.PI) / 180;
    const height = 2 * Math.tan(fov / 2) * this.camera.position.z;
    const width = height * this.camera.aspect;
    this.viewport = { width, height };

    this.medias?.forEach(media => media.onResize({ screen: this.screen, viewport: this.viewport }));
  }

  onTouchDown(e: MouseEvent | TouchEvent) {
    this.isDown = true;
    this.scroll.position = this.scroll.current;
    this.start = e instanceof TouchEvent ? e.touches[0].clientY : e.clientY;
  }

  onTouchMove(e: MouseEvent | TouchEvent) {
    if (!this.isDown || this.scroll.position === undefined) return;
    const y = e instanceof TouchEvent ? e.touches[0].clientY : e.clientY;
    const distance = (this.start - y) * 0.1;
    this.scroll.target = this.scroll.position + distance;
  }

  onTouchUp() {
    this.isDown = false;
  }

  onWheel(e: WheelEvent) {
    this.scroll.target += e.deltaY * 0.005;
  }

  update() {
    this.scroll.current = lerp(this.scroll.current, this.scroll.target, this.scroll.ease);
    this.medias?.forEach(media => media.update(this.scroll));
    this.renderer.render({ scene: this.scene, camera: this.camera });
    this.scroll.last = this.scroll.current;
    this.rafId = requestAnimationFrame(this.update);
  }

  addEventListeners() {
    window.addEventListener('resize', this.onResize);
    window.addEventListener('wheel', this.onWheel, { passive: false });
    window.addEventListener('mousedown', this.onTouchDown);
    window.addEventListener('mousemove', this.onTouchMove);
    window.addEventListener('mouseup', this.onTouchUp);
    window.addEventListener('touchstart', this.onTouchDown as EventListener, { passive: false });
    window.addEventListener('touchmove', this.onTouchMove as EventListener, { passive: false });
    window.addEventListener('touchend', this.onTouchUp as EventListener);
  }

  destroy() {
    window.removeEventListener('resize', this.onResize);
    window.removeEventListener('wheel', this.onWheel);
    window.removeEventListener('mousedown', this.onTouchDown);
    window.removeEventListener('mousemove', this.onTouchMove);
    window.removeEventListener('mouseup', this.onTouchUp);
    window.removeEventListener('touchstart', this.onTouchDown as EventListener);
    window.removeEventListener('touchmove', this.onTouchMove as EventListener);
    window.removeEventListener('touchend', this.onTouchUp as EventListener);
    cancelAnimationFrame(this.rafId);
  }
}

export interface FlyingPostersProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Array of image URLs to display */
  items?: string[];
  /** Width of the individual poster planes in pixels */
  planeWidth?: number;
  /** Height of the individual poster planes in pixels */
  planeHeight?: number;
  /** Intensity of the 3D distortion effect */
  distortion?: number;
  /** Smoothness of the scroll (lower is smoother) */
  scrollEase?: number;
  /** Camera Field of View */
  cameraFov?: number;
  /** Camera Z position */
  cameraZ?: number;
}

/**
 * FlyingPosters - A high-end 3D vertical gallery
 * 
 * Demonstrates a premium motion aesthetic with WebGL distortion and smooth scrolling.
 */
export function FlyingPosters({
  items = [
    'https://picsum.photos/500/500?grayscale&sig=1',
    'https://picsum.photos/600/600?grayscale&sig=2',
    'https://picsum.photos/400/400?grayscale&sig=3',
    'https://picsum.photos/500/700?grayscale&sig=4',
    'https://picsum.photos/700/500?grayscale&sig=5',
  ],
  planeWidth = 320,
  planeHeight = 440,
  distortion = 3,
  scrollEase = 0.05,
  cameraFov = 45,
  cameraZ = 20,
  className = '',
  ...props
}: FlyingPostersProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const instanceRef = useRef<Canvas | null>(null);

  useEffect(() => {
    if (!containerRef.current || !canvasRef.current) return;

    // Use a small delay to ensure container dimensions are settled
    const timeoutId = setTimeout(() => {
      if (!containerRef.current || !canvasRef.current) return;
      instanceRef.current = new Canvas({
        container: containerRef.current,
        canvas: canvasRef.current,
        items,
        planeWidth,
        planeHeight,
        distortion,
        scrollEase,
        cameraFov,
        cameraZ
      });
    }, 100);

    return () => {
      clearTimeout(timeoutId);
      instanceRef.current?.destroy();
      instanceRef.current = null;
    };
  }, [items, planeWidth, planeHeight, distortion, scrollEase, cameraFov, cameraZ]);

  return (
    <div 
      ref={containerRef} 
      className={`w-full h-full overflow-hidden relative select-none bg-background ${className}`} 
      {...props}
    >
      <canvas ref={canvasRef} className="block w-full h-full" />
    </div>
  );
}

export default FlyingPosters;
~~~

Implementation Guidelines

1. Analyze the component structure, styling, animation implementations
2. Review the component's arguments and state
3. Think through what is the best place to adopt this component/style into the design we are doing
4. Then adopt the component/design to our current system

Help me integrate this into my design
