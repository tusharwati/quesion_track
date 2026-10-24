export interface Question {
  id: string;
  raw_text: string;
  corrected_text: string;
  is_question: boolean;
  confidence: number;
  processing_time: number;
  created_at: string;
}

export interface TranscriptionResult {
  raw_text: string;
  corrected_text: string;
  is_question: boolean;
  confidence: number;
  processing_time: number;
}

export interface Settings {
  stt_model: 'tiny' | 'base' | 'small';
  language: string;
  recent_question_count: 1 | 2 | 3 | 5;
  auto_correction: boolean;
  question_detection: boolean;
  theme: 'light' | 'dark' | 'system';
}

export interface SystemStatus {
  status: 'ready' | 'listening' | 'processing' | 'error';
  model_loaded: boolean;
  microphone_available: boolean;
  message?: string;
}

export interface AudioUpload {
  file: File;
  duration?: number;
}

export interface HealthCheck {
  status: string;
  model_loaded: boolean;
  database_connected: boolean;
  version: string;
}

export interface ApiError {
  detail: string;
  error_code?: string;
}

export type RecordingState = 'idle' | 'recording' | 'processing' | 'completed' | 'error';
