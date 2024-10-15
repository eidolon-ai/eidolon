'use client'

import React from 'react';
import { Loader } from 'lucide-react';

interface CircularProgressWithContentProps {
  value?: number;
  size?: number;
  color?: string;
  className?: string;
  children: React.ReactNode;
}

export function CircularProgressWithContent({
  value = 0,
  size = 40,
  color = 'blue',
  className = '',
  children
}: CircularProgressWithContentProps) {
  // Calculate the stroke dash offset based on the value
  const circumference = 2 * Math.PI * 16; // Lucide's Loader has a default radius of 16
  const strokeDashoffset = ((100 - value) / 100 * circumference).toFixed(3);

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <Loader
        size={size}
        className={`text-${color}-600 animate-spin`}
        strokeWidth={4}
        style={{
          strokeDasharray: circumference,
          strokeDashoffset: strokeDashoffset
        }}
      />
      <div className="absolute top-0 left-0 flex items-center justify-center w-full h-full">
        {children}
      </div>
    </div>
  );
}