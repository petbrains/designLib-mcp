You are given a task to integrate an existing React component in the codebase

The codebase should support:
- shadcn project structure  
- Tailwind CSS
- Typescript

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind or Typescript.

Determine the default path for components and styles. 
If default path for components is not /components/ui, provide instructions on why it's important to create this folder
Copy-paste this component to /components/ui folder:
```tsx
3d-sliding-cards.tsx
'use client'

import { useEffect, useState } from 'react'
import '../../index.css'

type Card = {
  id: number
  imgSrc: string
}

export default function FloatingCards() {
  const [cards, setCards] = useState<Card[]>([])

  useEffect(() => {
    // Use your custom images
    const images: string[] = [
      'https://picsum.photos/400/300?random=2',
      'https://picsum.photos/400/300?random=4',
      'https://picsum.photos/400/300?random=6',
      'https://picsum.photos/400/300?random=8',
      'https://picsum.photos/400/300?random=10',
      'https://picsum.photos/400/300?random=12',
    ]

    const newCards = images.map((img, index) => ({
      id: index + 1,
      imgSrc: img,
    }))
    
    setCards(newCards)

    // Scroll handler applying vertical movement to the slider
    const handleScroll = () => {
      const scrollPos = window.scrollY
      const slider = document.querySelector('.slider') as HTMLElement | null
      if (!slider) return

      const initialTransform =
        'translate3d(-50%, -50%, 0) rotateX(0deg) rotateY(-25deg) rotateZ(-120deg)'
      const zOffset = scrollPos * 0.5
      slider.style.transform = `${initialTransform} translateY(${zOffset}px)`
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    // Set initial transform once on mount
    handleScroll()

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  // Mouse interactions per card
  const handleMouseOver = (e: React.MouseEvent<HTMLDivElement>) => {
    e.currentTarget.style.left = '15%'
  }

  const handleMouseOut = (e: React.MouseEvent<HTMLDivElement>) => {
    e.currentTarget.style.left = '0%'
  }

  return (
    <div className="slider" aria-label="3D image slider">
      {cards.map((card) => (
        <div
          key={card.id}
          className="card"
          onMouseOver={handleMouseOver}
          onMouseOut={handleMouseOut}
        >
          <img 
            src={card.imgSrc || "/placeholder.svg"} 
            alt={`Image ${card.id}`}
            loading="lazy"
          />
        </div>
      ))}
    </div>
  )
}

demo.tsx
import FloatingCards from "@/components/ui/3d-sliding-cards";

export default function DemoOne() {
  return <FloatingCards />;
}

```

Implementation Guidelines
 1. Analyze the component structure and identify all required dependencies
 2. Review the component's argumens and state
 3. Identify any required context providers or hooks and install them
 4. Questions to Ask
 - What data/props will be passed to this component?
 - Are there any specific state management requirements?
 - Are there any required assets (images, icons, etc.)?
 - What is the expected responsive behavior?
 - What is the best place to use this component in the app?

Steps to integrate
 0. Copy paste all the code above in the correct directories
 1. Install external dependencies
 2. Fill image assets with Unsplash stock images you know exist
 3. Use lucide-react icons for svgs or logos if component requires them
