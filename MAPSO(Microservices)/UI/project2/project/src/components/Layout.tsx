import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, FileText, Activity, BarChart3, Sun, Moon } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { theme, toggleTheme } = useTheme();
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'bg-primary/10 text-primary' : 'text-foreground/70 hover:bg-muted/10';
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-card border-b border-border shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Shield className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-bold">DocuSecure</h1>
          </div>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full hover:bg-muted/10"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Main content */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-16 md:w-64 border-r border-border bg-card">
          <nav className="p-2 md:p-4 flex flex-col space-y-2">
            <Link 
              to="/" 
              className={`flex items-center space-x-2 rounded-md p-2 ${isActive('/')}`}
            >
              <FileText className="w-5 h-5" />
              <span className="hidden md:inline">Upload Document</span>
            </Link>
            <Link 
              to="/status" 
              className={`flex items-center space-x-2 rounded-md p-2 ${isActive('/status')}`}
            >
              <Activity className="w-5 h-5" />
              <span className="hidden md:inline">Check Status</span>
            </Link>
            {/* <Link 
              to="/logs" 
              className={`flex items-center space-x-2 rounded-md p-2 ${isActive('/logs')}`}
            >
              <BarChart3 className="w-5 h-5" />
              <span className="hidden md:inline">Logs</span>
            </Link> */}
          </nav>
        </aside>

        {/* Content */}
        <main className="flex-1 p-4 md:p-8 overflow-auto">
          <div className="container mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;