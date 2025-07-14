import React, { forwardRef, useRef, useState } from 'react';
import { UploadCloud, X, FileText } from 'lucide-react';
import Button from './Button';
import clsx from 'clsx';

interface FileInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type' | 'value' | 'onChange'> {
  label?: string;
  accept?: string;
  error?: string;
  value?: File | null;
  onChange?: (file: File | null) => void;
  fullWidth?: boolean;
}

const FileInput = forwardRef<HTMLInputElement, FileInputProps>(
  ({ label, accept, error, value, onChange, fullWidth = false, className, ...props }, forwardedRef) => {
    const inputRef = useRef<HTMLInputElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0] || null;
      onChange?.(file);
    };

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(true);
    };

    const handleDragLeave = () => {
      setIsDragging(false);
    };

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(false);
      
      const file = event.dataTransfer.files?.[0] || null;
      if (file) {
        onChange?.(file);
        
        // Update the input value to match the dropped file
        if (inputRef.current) {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          inputRef.current.files = dataTransfer.files;
        }
      }
    };

    const handleBrowseClick = () => {
      inputRef.current?.click();
    };

    const handleClearFile = () => {
      onChange?.(null);
      if (inputRef.current) {
        inputRef.current.value = '';
      }
    };

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label className="block text-sm font-medium mb-1">
            {label}
          </label>
        )}
        <div
          className={clsx(
            'relative border-2 border-dashed rounded-md p-4 transition-colors',
            isDragging ? 'border-primary bg-primary/5' : 'border-border',
            error ? 'border-error' : '',
            fullWidth && 'w-full',
            className
          )}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input
            ref={(node) => {
              // Handle both the forwardedRef and our internal ref
              if (typeof forwardedRef === 'function') {
                forwardedRef(node);
              } else if (forwardedRef) {
                forwardedRef.current = node;
              }
              inputRef.current = node;
            }}
            type="file"
            accept={accept}
            className="sr-only"
            onChange={handleFileChange}
            {...props}
          />

          {value ? (
            <div className="flex items-center justify-between p-2 bg-muted/10 rounded">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-primary" />
                <span className="text-sm truncate max-w-xs">{value.name}</span>
              </div>
              <button
                type="button"
                onClick={handleClearFile}
                className="text-muted hover:text-error focus:outline-none"
                aria-label="Remove file"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <div className="text-center p-4">
              <UploadCloud className="mx-auto h-12 w-12 text-muted" />
              <div className="mt-2">
                <p className="text-sm text-foreground font-medium">
                  Drag and drop your file here, or
                </p>
                <p className="text-xs text-muted mt-1">
                  Supported file types: PDF, DOCX, and more
                </p>
              </div>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleBrowseClick}
                className="mt-3"
              >
                Browse Files
              </Button>
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-sm text-error">{error}</p>
        )}
      </div>
    );
  }
);

FileInput.displayName = 'FileInput';

export default FileInput;