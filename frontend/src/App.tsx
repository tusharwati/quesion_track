import { useEffect, useState } from 'react';
import { Settings } from 'lucide-react';
import {
  AppShell,
  AudioRecorder,
  LatestQuestions,
  QuestionHistory,
  SettingsPanel,
  TranscriptPanel,
} from '@/components';
import { useStore } from '@/hooks/useStore';
import { healthApi } from '@/services/api';

function App() {
  const { theme, setSystemStatus, setQuestions, settings } = useStore();
  const [settingsOpen, setSettingsOpen] = useState(false);
  
  useEffect(() => {
    // Apply theme
    document.documentElement.classList.toggle('dark', theme === 'dark');
    
    // Check system health
    const checkHealth = async () => {
      try {
        const health = await healthApi.check();
        setSystemStatus({
          status: health.model_loaded ? 'ready' : 'error',
          model_loaded: health.model_loaded,
          microphone_available: true, // Will be checked when recording starts
        });
      } catch (error) {
        setSystemStatus({
          status: 'error',
          model_loaded: false,
          microphone_available: false,
          message: 'Backend not available',
        });
      }
    };
    
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    
    return () => clearInterval(interval);
  }, [theme, setSystemStatus]);
  
  return (
    <AppShell>
      <div className="flex justify-end mb-4">
        <button
          onClick={() => setSettingsOpen(true)}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Open settings"
        >
          <Settings className="w-5 h-5 text-gray-600 dark:text-gray-300" />
        </button>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column - Audio Input and Transcript */}
        <div className="lg:col-span-2 space-y-6">
          <AudioRecorder />
          <TranscriptPanel />
        </div>
        
        {/* Right column - Latest Questions */}
        <div className="lg:col-span-1">
          <LatestQuestions />
        </div>
      </div>
      
      {/* Question History - Full width below */}
      <div className="mt-6">
        <QuestionHistory />
      </div>
      
      <SettingsPanel isOpen={settingsOpen} onClose={() => setSettingsOpen(false)} />
    </AppShell>
  );
}

export default App;
