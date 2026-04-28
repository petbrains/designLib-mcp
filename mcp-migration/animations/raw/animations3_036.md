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
testimonial-card.tsx
import React from 'react';
// Assuming you have these libraries. If not, run:
// npm install lucide-react framer-motion
// You'll also need Tailwind CSS set up in your project.
import { Star } from 'lucide-react';
import { motion } from 'framer-motion';

/**
 * A reusable, high-quality, and animated testimonial card component.
 *
 * @param {{
 * quote: string;
 * authorName: string;
 * authorTitle: string;
 * avatarUrl: string;
 * rating: number;
 * index: number; // Index for staggered animation
 * }} props - The props for the component.
 * @returns {JSX.Element} The rendered testimonial card.
 */
const TestimonialCard = ({
  quote,
  authorName,
  authorTitle,
  avatarUrl,
  rating,
  index,
}) => {
  // Animation variants for Framer Motion
  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        delay: index * 0.1, // Staggered delay based on index
        ease: "easeOut",
      },
    },
  };

  return (
    <motion.div
      className="flex h-full flex-col justify-between rounded-2xl bg-white p-8 shadow-sm dark:bg-gray-800"
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover={{ scale: 1.03, boxShadow: "0px 10px 20px rgba(0,0,0,0.1)" }}
      transition={{ duration: 0.2 }}
    >
      <div>
        <div className="flex items-center">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={`h-5 w-5 ${
                i < rating ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'
              }`}
              fill="currentColor"
            />
          ))}
        </div>
        <blockquote className="mt-6 text-lg leading-relaxed text-gray-600 dark:text-gray-300">
          <p>"{quote}"</p>
        </blockquote>
      </div>
      <footer className="mt-8">
        <div className="flex items-center">
          <img
            className="h-12 w-12 flex-shrink-0 rounded-full object-cover"
            src={avatarUrl}
            alt={`Avatar of ${authorName}`}
            onError={(e) => {
                e.currentTarget.src = `https://placehold.co/48x48/E2E8F0/4A5568?text=${authorName.charAt(0)}`;
                e.currentTarget.onerror = null;
            }}
          />
          <div className="ml-4">
            <p className="font-semibold text-gray-900 dark:text-white">
              {authorName}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {authorTitle}
            </p>
          </div>
        </div>
      </footer>
    </motion.div>
  );
};
export default TestimonialCard;

demo.tsx
import TestimonialCard from "@/components/ui/testimonial-card";

export default function DemoOne() {
  const testimonials = [
    {
      quote:
        "This is a game-changer. The platform is intuitive, powerful, and has completely transformed our workflow. The support team is also incredibly responsive.",
      authorName: 'Sarah Johnson',
      authorTitle: 'CEO, Innovate Inc.',
      avatarUrl: 'https://i.pravatar.cc/150?img=1',
      rating: 5,
    },
    {
      quote:
        'I was skeptical at first, but the results speak for themselves. Our productivity is up by 40% and the team is happier than ever. Highly recommended!',
      authorName: 'Michael Chen',
      authorTitle: 'CTO, Tech Solutions',
      avatarUrl: 'https://i.pravatar.cc/150?img=2',
      rating: 5,
    },
    {
      quote:
        "An essential tool for any modern business. It's flexible enough to adapt to our unique needs, and the feature set is constantly growing and improving.",
      authorName: 'Emily Rodriguez',
      authorTitle: 'Marketing Director, Creative Co.',
      avatarUrl: 'https://i.pravatar.cc/150?img=3',
      rating: 4,
    },
  ];

  return (
    <div className="min-h-screen w-full bg-gray-100 font-sans antialiased dark:bg-gray-900">
      <div className="container mx-auto px-4 py-16 sm:py-24">
        <header className="mb-16 text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl dark:text-white">
            What Our Customers Are Saying
          </h1>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-600 dark:text-gray-400">
            We're trusted by thousands of amazing companies. Read what they think about us.
          </p>
        </header>

        <div className="mx-auto grid max-w-7xl grid-cols-1 gap-10 md:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <TestimonialCard key={index} {...testimonial} index={index} />
          ))}
        </div>
      </div>
    </div>
  );
}



```

Install NPM dependencies:
```bash
lucide-react, framer-motion
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
