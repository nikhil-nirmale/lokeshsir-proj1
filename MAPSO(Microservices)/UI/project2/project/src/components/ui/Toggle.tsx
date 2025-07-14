import React, { useState } from 'react';
import clsx from 'clsx';

interface ToggleProps {
  label: string;
  description?: string;
  defaultChecked?: boolean;
  onChange?: (checked: boolean) => void;
  disabled?: boolean;
}

const Toggle: React.FC<ToggleProps> = ({
  label,
  description,
  defaultChecked = false,
  onChange,
  disabled = false,
}) => {
  const [checked, setChecked] = useState(defaultChecked);

  const handleToggle = () => {
    if (disabled) return;
    
    const newChecked = !checked;
    setChecked(newChecked);
    onChange?.(newChecked);
  };

  return (
    <div className="flex items-start">
      <button
        type="button"
        className={clsx(
          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2',
          checked ? 'bg-primary' : 'bg-muted',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
        role="switch"
        aria-checked={checked}
        onClick={handleToggle}
        disabled={disabled}
      >
        <span className="sr-only">Toggle {label}</span>
        <span
          className={clsx(
            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
            checked ? 'translate-x-5' : 'translate-x-0'
          )}
        />
      </button>
      <div className="ml-3">
        <span className="text-sm font-medium text-foreground">{label}</span>
        {description && (
          <p className="text-sm text-muted">{description}</p>
        )}
      </div>
    </div>
  );
};

export default Toggle;