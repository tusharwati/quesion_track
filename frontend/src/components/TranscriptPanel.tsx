import { Copy, CheckCircle } from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/utils';
import { useStore } from '@/hooks/useStore';

export function TranscriptPanel() {
  const { questions, recordingState } = useStore();
  const [copied, setCopied] = useState(false);
  
  const latestQuestion = questions[0];
  
  const handleCopy = async () => {
    if (!latestQuestion) return;
    
    await navigator.clipboard.writeText(latestQuestion.corrected_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Transcript
        </h2>
        {latestQuestion && (
          <button
            onClick={handleCopy}
            className={cn(
              "flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
              "hover:bg-gray-100 dark:hover:bg-gray-700",
              copied && "text-green-600 dark:text-green-400"
            )}
          >
            {copied ? (
              <>
                <CheckCircle className="w-4 h-4" />
                Copied
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy
              </>
            )}
          </button>
        )}
      </div>
      
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
            Raw Transcript
          </label>
          <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg min-h-[80px]">
            {latestQuestion ? (
              <p className="text-gray-700 dark:text-gray-300 font-mono text-sm">
                {latestQuestion.raw_text}
              </p>
            ) : (
              <p className="text-gray-400 dark:text-gray-600 italic">
                No transcription yet. Start recording or upload an audio file.
              </p>
            )}
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
            Corrected Question
          </label>
          <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg min-h-[80px]">
            {latestQuestion ? (
              <p className="text-gray-900 dark:text-white font-medium">
                {latestQuestion.corrected_text}
              </p>
            ) : (
              <p className="text-gray-400 dark:text-gray-600 italic">
                Corrected question will appear here after transcription.
              </p>
            )}
          </div>
        </div>
        
        {latestQuestion && (
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div>
              <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                Confidence
              </p>
              <p className="text-sm font-semibold text-gray-900 dark:text-white">
                {(latestQuestion.confidence * 100).toFixed(0)}%
              </p>
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                Processing Time
              </p>
              <p className="text-sm font-semibold text-gray-900 dark:text-white">
                {latestQuestion.processing_time.toFixed(2)}s
              </p>
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">
                Detected
              </p>
              <p className="text-sm font-semibold text-gray-900 dark:text-white">
                {latestQuestion.is_question ? 'Question' : 'Statement'}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
