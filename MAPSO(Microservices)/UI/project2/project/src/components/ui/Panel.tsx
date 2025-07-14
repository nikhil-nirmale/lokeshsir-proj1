import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import clsx from 'clsx';

interface PanelProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
  className?: string;
  headerClassName?: string;
  variant?: 'default' | 'success' | 'warning' | 'error';
}

const Panel: React.FC<PanelProps> = ({
  title,
  children,
  defaultOpen = false,
  className = '',
  headerClassName = '',
  variant = 'default',
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const toggleOpen = () => setIsOpen(!isOpen);

  const variantClasses = {
    default: 'bg-card border-border',
    success: 'bg-success/10 border-success/20',
    warning: 'bg-warning/10 border-warning/20',
    error: 'bg-error/10 border-error/20',
  };

  const headerVariantClasses = {
    default: 'text-foreground',
    success: 'text-success-dark',
    warning: 'text-warning-dark',
    error: 'text-error-dark',
  };

  return (
    <div className={clsx('border rounded-md overflow-hidden', variantClasses[variant], className)}>
      <button
        className={clsx(
          'w-full flex items-center justify-between p-4 text-left font-medium focus:outline-none focus:ring-2 focus:ring-primary focus:ring-inset',
          headerVariantClasses[variant],
          headerClassName
        )}
        onClick={toggleOpen}
        aria-expanded={isOpen}
      >
        <span>{title}</span>
        {isOpen ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
      </button>
      <div
        className={clsx(
          'overflow-hidden transition-all duration-200 ease-in-out',
          isOpen ? 'max-h-screen animate-fade-in' : 'max-h-0'
        )}
      >
        <div className="p-4 border-t border-border">{children}</div>
      </div>
    </div>
  );
};

export default Panel;