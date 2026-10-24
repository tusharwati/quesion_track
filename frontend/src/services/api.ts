import axios from 'axios';
import type { Question, TranscriptionResult, Settings, HealthCheck } from '@/types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const transcriptionApi = {
  transcribe: async (file: File): Promise<TranscriptionResult> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<TranscriptionResult>('/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
  
  createQuestion: async (
    raw_text: string,
    corrected_text: string,
    is_question: boolean = true,
    confidence: number = 0.9,
    processing_time: number = 0.0
  ): Promise<Question> => {
    const response = await api.post<Question>('/questions', null, {
      params: {
        raw_text,
        corrected_text,
        is_question,
        confidence,
        processing_time,
      },
    });
    
    return response.data;
  },
};

export const questionsApi = {
  list: async (skip: number = 0, limit: number = 100, search?: string): Promise<{ questions: Question[]; total: number }> => {
    const response = await api.get<{ questions: Question[]; total: number }>('/questions', {
      params: { skip, limit, search },
    });
    
    return response.data;
  },
  
  getRecent: async (count: number = 2): Promise<Question[]> => {
    const response = await api.get<Question[]>('/questions/recent', {
      params: { count },
    });
    
    return response.data;
  },
  
  delete: async (id: number): Promise<{ message: string; id: number }> => {
    const response = await api.delete<{ message: string; id: number }>(`/questions/${id}`);
    
    return response.data;
  },
  
  clearAll: async (): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>('/questions');
    
    return response.data;
  },
};

export const settingsApi = {
  get: async (): Promise<Settings> => {
    const response = await api.get<Settings>('/settings');
    
    return response.data;
  },
  
  update: async (settings: Partial<Settings>): Promise<Settings> => {
    const response = await api.put<Settings>('/settings', settings);
    
    return response.data;
  },
};

export const healthApi = {
  check: async (): Promise<HealthCheck> => {
    const response = await api.get<HealthCheck>('/health');
    
    return response.data;
  },
};

export default api;
