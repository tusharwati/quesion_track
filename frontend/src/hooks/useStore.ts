import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Question, Settings, RecordingState, SystemStatus } from '@/types';

interface AppState {
  // Questions
  questions: Question[];
  recentQuestions: Question[];
  setQuestions: (questions: Question[]) => void;
  addQuestion: (question: Question) => void;
  removeQuestion: (id: string) => void;
  clearQuestions: () => void;
  
  // Recording
  recordingState: RecordingState;
  setRecordingState: (state: RecordingState) => void;
  recordingDuration: number;
  setRecordingDuration: (duration: number) => void;
  
  // Settings
  settings: Settings;
  updateSettings: (settings: Partial<Settings>) => void;
  
  // System Status
  systemStatus: SystemStatus;
  setSystemStatus: (status: SystemStatus) => void;
  
  // UI State
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
}

const defaultSettings: Settings = {
  stt_model: 'base',
  language: 'en',
  recent_question_count: 2,
  auto_correction: true,
  question_detection: true,
  theme: 'light',
};

const defaultSystemStatus: SystemStatus = {
  status: 'ready',
  model_loaded: false,
  microphone_available: false,
};

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      // Questions
      questions: [],
      recentQuestions: [],
      setQuestions: (questions) => set({ questions }),
      addQuestion: (question) =>
        set((state) => ({
          questions: [question, ...state.questions],
          recentQuestions: [question, ...state.recentQuestions].slice(0, state.settings.recent_question_count),
        })),
      removeQuestion: (id) =>
        set((state) => ({
          questions: state.questions.filter((q) => q.id !== id),
          recentQuestions: state.recentQuestions.filter((q) => q.id !== id),
        })),
      clearQuestions: () => set({ questions: [], recentQuestions: [] }),
      
      // Recording
      recordingState: 'idle',
      setRecordingState: (state) => set({ recordingState: state }),
      recordingDuration: 0,
      setRecordingDuration: (duration) => set({ recordingDuration: duration }),
      
      // Settings
      settings: defaultSettings,
      updateSettings: (newSettings) =>
        set((state) => ({
          settings: { ...state.settings, ...newSettings },
        })),
      
      // System Status
      systemStatus: defaultSystemStatus,
      setSystemStatus: (status) => set({ systemStatus: status }),
      
      // UI State
      theme: 'light',
      setTheme: (theme) => set({ theme }),
      sidebarOpen: true,
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
    }),
    {
      name: 'questiontrack-storage',
      partialize: (state) => ({
        settings: state.settings,
        theme: state.theme,
      }),
    }
  )
);
