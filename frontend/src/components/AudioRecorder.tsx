import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Mic, Square, Upload, Loader2 } from 'lucide-react';
import { cn, formatDuration } from '@/utils';
import { useStore } from '@/hooks/useStore';
import { transcriptionApi } from '@/services/api';
import type { RecordingState } from '@/types';

export function AudioRecorder() {
  const {
    recordingState,
    setRecordingState,
    recordingDuration,
    setRecordingDuration,
    addQuestion,
    settings,
    systemStatus,
    setSystemStatus,
  } = useStore();
  
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number>(0);
  
  const startRecording = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };
      
      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach(track => track.stop());
        
        const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const file = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
        
        setRecordingState('processing');
        
        try {
          const result = await transcriptionApi.transcribe(file);
          
          if (result.is_question) {
            addQuestion({
              id: Date.now().toString(),
              raw_text: result.raw_text,
              corrected_text: result.corrected_text,
              is_question: result.is_question,
              confidence: result.confidence,
              processing_time: result.processing_time,
              created_at: new Date().toISOString(),
            });
          }
          
          setRecordingState('completed');
          setTimeout(() => setRecordingState('idle'), 2000);
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Transcription failed');
          setRecordingState('error');
          setSystemStatus({ ...systemStatus, status: 'error' });
        }
      };
      
      mediaRecorder.start(1000);
      startTimeRef.current = Date.now();
      setRecordingState('listening');
      
      timerRef.current = setInterval(() => {
        const elapsed = (Date.now() - startTimeRef.current) / 1000;
        setRecordingDuration(elapsed);
      }, 100);
      
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Microphone access denied';
      setError(message);
      setRecordingState('error');
    }
  }, [addQuestion, setRecordingDuration, setRecordingState, setSystemStatus, settings, systemStatus]);
  
  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  }, []);
  
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    setRecordingState('processing');
    setError(null);
    
    try {
      const result = await transcriptionApi.transcribe(file);
      
      if (result.is_question) {
        addQuestion({
          id: Date.now().toString(),
          raw_text: result.raw_text,
          corrected_text: result.corrected_text,
          is_question: result.is_question,
          confidence: result.confidence,
          processing_time: result.processing_time,
          created_at: new Date().toISOString(),
        });
      }
      
      setRecordingState('completed');
      setTimeout(() => setRecordingState('idle'), 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Transcription failed');
      setRecordingState('error');
    }
    
    event.target.value = '';
  };
  
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);
  
  const isRecording = recordingState === 'listening';
  const isProcessing = recordingState === 'processing';
  
  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Audio Input
      </h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}
      
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Status: <span className="font-normal text-gray-600 dark:text-gray-400">{recordingState}</span>
          </span>
          
          {isRecording && (
            <span className="text-sm font-mono text-gray-600 dark:text-gray-400">
              {formatDuration(recordingDuration)}
            </span>
          )}
        </div>
        
        <div className="flex flex-wrap gap-3">
          {!isRecording && !isProcessing && (
            <>
              <button
                onClick={startRecording}
                disabled={recordingState === 'processing'}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors",
                  "bg-red-600 text-white hover:bg-red-700",
                  "focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2",
                  "disabled:opacity-50 disabled:cursor-not-allowed"
                )}
                aria-label="Start recording"
              >
                <Mic className="w-5 h-5" />
                Start Recording
              </button>
              
              <label
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg font-medium cursor-pointer",
                  "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600",
                  "transition-colors border border-gray-300 dark:border-gray-600"
                )}
              >
                <Upload className="w-5 h-5" />
                Upload Audio
                <input
                  type="file"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={isProcessing}
                />
              </label>
            </>
          )}
          
          {isRecording && (
            <button
              onClick={stopRecording}
              className={cn(
                "flex items-center gap-2 px-4 py-2 rounded-lg font-medium",
                "bg-gray-900 text-white hover:bg-gray-800 dark:bg-gray-600 dark:hover:bg-gray-500",
                "transition-colors"
              )}
              aria-label="Stop recording"
            >
              <Square className="w-5 h-5" />
              Stop Recording
            </button>
          )}
          
          {isProcessing && (
            <div className="flex items-center gap-2 px-4 py-2 bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400 rounded-lg">
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing audio...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
