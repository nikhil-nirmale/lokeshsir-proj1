import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import Button from '../components/ui/Button';

const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-4">
      <AlertCircle className="w-16 h-16 text-error mb-4" />
      <h1 className="text-3xl font-bold mb-2">404 - Page Not Found</h1>
      <p className="text-muted max-w-md mb-6">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Link to="/">
        <Button variant="primary">Return to Home</Button>
      </Link>
    </div>
  );
};

export default NotFoundPage;