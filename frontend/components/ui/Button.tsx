'use client';

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost' | 'link' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', children, ...props }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 font-sans shadow-sm hover:shadow-md';

    const variantClasses = {
      primary: 'bg-[#1C352D] text-white hover:bg-[#1C352D]/90',
      secondary: 'bg-[#A6B28B] text-white hover:bg-[#A6B28B]/80',
      accent: 'bg-[#F5C9B0] text-white hover:bg-[#F5C9B0]/90',
      ghost: 'hover:bg-[#F5C9B0] hover:text-[#1C352D]',
      link: 'underline-offset-4 hover:underline text-[#1C352D]',
      outline: 'border border-[#1C352D] text-[#1C352D] hover:bg-[#1C352D] hover:text-white',
    };

    const sizeClasses = {
      sm: 'h-9 rounded-md px-3',
      md: 'h-10 py-2 px-4',
      lg: 'h-11 rounded-md px-8',
    };

    const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;

    return (
      <button
        className={classes}
        ref={ref}
        {...props}
      >
        {children}
      </button>
    );
  }
);
Button.displayName = 'Button';

export { Button };