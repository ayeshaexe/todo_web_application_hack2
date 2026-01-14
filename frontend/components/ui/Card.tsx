'use client';

import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

const Card = ({ children, className = '', ...props }: CardProps) => {
  return (
    <div
      className={`vintage-card rounded-lg border bg-card text-card-foreground shadow-sm p-6 font-sans ${className}`}
      role="region"
      {...props}
    >
      {children}
    </div>
  );
};

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

const CardHeader = ({ children, className = '', ...props }: CardHeaderProps) => {
  return (
    <div className={`flex flex-col space-y-1.5 p-2 font-sans ${className}`} {...props}>
      {children}
    </div>
  );
};

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
  className?: string;
}

const CardTitle = ({ children, className = '', ...props }: CardTitleProps) => {
  return (
    <h3
      className={`text-2xl font-semibold leading-none tracking-tight text-[#1C352D] font-sans ${className}`}
      {...props}
    >
      {children}
    </h3>
  );
};

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

const CardContent = ({ children, className = '', ...props }: CardContentProps) => {
  return (
    <div className={`p-6 pt-0 ${className}`} {...props}>
      {children}
    </div>
  );
};

export { Card, CardHeader, CardTitle, CardContent };