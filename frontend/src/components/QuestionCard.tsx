import { Copy, Trash2, Clock } from 'lucide-react';
import { useState } from 'react';
import { cn, formatTimestamp } from '@/utils';
import type { Question } from '@/types';

interface QuestionCardProps {
  question: Question;
  onCopy?: () => void;
  onDelete?: (id: string) => void;
  showRaw?: boolean;
}

export function QuestionCard({ question, onCopy, onDelete, showRaw = false }: QuestionCardProps) {
  const [copied, setCopied] = useState(false);
  
  const handleCopy = async () => {
    const text = showRaw ? question.raw_text : question.corrected_text;
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
    onCopy?.();
  };
  
  const handleDelete = () => {
    onDelete?.(question.id);
  };
  
  return (
    <div className="card p-4 mb-3">
      <div className="flex justify-between items-start gap-3">
        <div className="flex-1">
          {showRaw && (
            <div className="mb-2">
              <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                Raw
              </span>
              <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">
                {question.raw_text}
              </p>
            </div>
          )}
          
          <p className="text-gray-900 dark:text-white font-medium">
            {question.corrected_text}
          </p>
          
          <div className="flex items-center gap-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formatTimestamp(question.created_at)}
            </span>
            <span className="flex items-center gap-1">
              Confidence: {(question.confidence * 100).toFixed(0)}%
            </span>
            <span className="flex items-center gap-1">
              {question.processing_time.toFixed(2)}s
            </span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className={cn(
              "p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors",
              copied && "text-green-600 dark:text-green-400"
            )}
            aria-label={copied ? "Copied" : "Copy question"}
          >
            <Copy className="w-4 h-4" />
          </button>
          
          {onDelete && (
            <button
              onClick={handleDelete}
              className="p-2 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 transition-colors"
              aria-label="Delete question"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
