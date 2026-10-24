import { X, Settings as SettingsIcon } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useStore } from '@/hooks/useStore';
import { settingsApi } from '@/services/api';
import { cn } from '@/utils';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  const { settings, updateSettings } = useStore();
  const [localSettings, setLocalSettings] = useState(settings);
  const [saved, setSaved] = useState(false);
  
  useEffect(() => {
    loadSettings();
  }, []);
  
  const loadSettings = async () => {
    try {
      const result = await settingsApi.get();
      updateSettings(result);
      setLocalSettings(result);
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };
  
  const handleSave = async () => {
    try {
      const result = await settingsApi.update(localSettings);
      updateSettings(result);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      console.error('Failed to save settings:', error);
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:p-0">
        <div className="fixed inset-0 transition-opacity" onClick={onClose}>
          <div className="absolute inset-0 bg-gray-500 dark:bg-gray-900 opacity-75"></div>
        </div>
        
        <div className="inline-block w-full max-w-md p-6 my-8 text-left align-middle transition-all transform bg-white dark:bg-gray-800 shadow-xl rounded-lg">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <SettingsIcon className="w-5 h-5 text-gray-600 dark:text-gray-300" />
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Settings
              </h3>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              aria-label="Close settings"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Speech Model
              </label>
              <select
                value={localSettings.stt_model}
                onChange={(e) => setLocalSettings({ ...localSettings, stt_model: e.target.value as any })}
                className="input"
              >
                <option value="tiny">Tiny (fastest)</option>
                <option value="base">Base (balanced)</option>
                <option value="small">Small (most accurate)</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Recent Question Count
              </label>
              <select
                value={localSettings.recent_question_count}
                onChange={(e) => setLocalSettings({ ...localSettings, recent_question_count: parseInt(e.target.value) as any })}
                className="input"
              >
                <option value={1}>1 question</option>
                <option value={2}>2 questions</option>
                <option value={3}>3 questions</option>
                <option value={5}>5 questions</option>
              </select>
            </div>
            
            <div className="space-y-3">
              <label className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Auto Correction
                </span>
                <input
                  type="checkbox"
                  checked={localSettings.auto_correction}
                  onChange={(e) => setLocalSettings({ ...localSettings, auto_correction: e.target.checked })}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
              </label>
              
              <label className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Question Detection
                </span>
                <input
                  type="checkbox"
                  checked={localSettings.question_detection}
                  onChange={(e) => setLocalSettings({ ...localSettings, question_detection: e.target.checked })}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                />
              </label>
            </div>
          </div>
          
          <div className="mt-6 flex items-center justify-end gap-3">
            {saved && (
              <span className="text-sm text-green-600 dark:text-green-400">
                Settings saved
              </span>
            )}
            <button
              onClick={handleSave}
              className="btn-primary"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
