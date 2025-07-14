import React, { forwardRef } from 'react';
import clsx from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, fullWidth = false, className, ...props }, ref) => {
    const inputClasses = clsx(
      'rounded-md border bg-background px-3 py-2 text-foreground shadow-sm placeholder:text-muted/70 focus:outline-none focus:ring-1 focus:ring-primary',
      error ? 'border-error focus:border-error' : 'border-border focus:border-primary',
      fullWidth && 'w-full',
      className
    );

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium mb-1" htmlFor={props.id}>
            {label}
          </label>
        )}
        <input 
          ref={ref}
          className={inputClasses}
          {...props}
        />
        {error && (
          <p className="mt-1 text-sm text-error">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;