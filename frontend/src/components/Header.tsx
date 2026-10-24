import { Mic, Sun, Moon } from 'lucide-react';
import { useStore } from '@/hooks/useStore';
import { StatusIndicator } from './StatusIndicator';

export function Header() {
  const { theme, setTheme, systemStatus } = useStore();
  
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };
  
  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Mic className="w-6 h-6 text-primary-600" aria-hidden="true" />
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                QuestionTrack
              </h1>
            </div>
            <span className="hidden sm:inline text-sm text-gray-500 dark:text-gray-400">
              Speech transcription and question extraction
            </span>
          </div>
          
          <div className="flex items-center gap-4">
            <StatusIndicator 
              status={systemStatus.status} 
              modelLoaded={systemStatus.model_loaded}
            />
            
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
            >
              {theme === 'light' ? (
                <Moon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
              ) : (
                <Sun className="w-5 h-5 text-gray-600 dark:text-gray-300" />
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
