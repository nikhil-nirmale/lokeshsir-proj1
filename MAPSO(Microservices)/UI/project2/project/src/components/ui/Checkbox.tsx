import React, { forwardRef } from 'react';
import clsx from 'clsx';

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: string;
  description?: string;
  error?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, description, error, className, ...props }, ref) => {
    return (
      <div className="flex items-start">
        <div className="flex items-center h-5">
          <input
            ref={ref}
            type="checkbox"
            className={clsx(
              'h-4 w-4 rounded border-border text-primary focus:ring-primary',
              error && 'border-error',
              className
            )}
            {...props}
          />
        </div>
        <div className="ml-3 text-sm">
          <label className="font-medium text-foreground">{label}</label>
          {description && (
            <p className="text-muted">{description}</p>
          )}
          {error && (
            <p className="mt-1 text-sm text-error">{error}</p>
          )}
        </div>
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export default Checkbox;