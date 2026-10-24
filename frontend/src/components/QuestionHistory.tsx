import { Search, Trash2, History as HistoryIcon } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useStore } from '@/hooks/useStore';
import { QuestionCard } from './QuestionCard';
import { questionsApi } from '@/services/api';
import type { Question } from '@/types';
import { cn } from '@/utils';

export function QuestionHistory() {
  const { questions, setQuestions, removeQuestion } = useStore();
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  useEffect(() => {
    loadQuestions();
  }, []);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      loadQuestions(search);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [search]);
  
  const loadQuestions = async (searchTerm?: string) => {
    setIsLoading(true);
    try {
      const result = await questionsApi.list(0, 100, searchTerm);
      setQuestions(result.questions);
    } catch (error) {
      console.error('Failed to load questions:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleDelete = async (id: string) => {
    try {
      await questionsApi.delete(parseInt(id));
      removeQuestion(id);
    } catch (error) {
      console.error('Failed to delete question:', error);
    }
  };
  
  const handleClearAll = async () => {
    if (!confirm('Are you sure you want to delete all questions? This cannot be undone.')) {
      return;
    }
    
    try {
      await questionsApi.clearAll();
      setQuestions([]);
    } catch (error) {
      console.error('Failed to clear questions:', error);
    }
  };
  
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Question History
        </h2>
        {questions.length > 0 && (
          <button
            onClick={handleClearAll}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
        )}
      </div>
      
      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search questions..."
            className={cn(
              "w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg",
              "bg-white dark:bg-gray-700 text-gray-900 dark:text-white",
              "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent",
              "placeholder:text-gray-400"
            )}
          />
        </div>
      </div>
      
      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : questions.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-gray-400">
          <HistoryIcon className="w-12 h-12 mb-2 opacity-50" />
          <p className="text-sm">
            {search ? 'No questions match your search' : 'No question history yet'}
          </p>
        </div>
      ) : (
        <div className="max-h-[500px] overflow-y-auto space-y-3">
          {questions.map((question) => (
            <QuestionCard
              key={question.id}
              question={question}
              onDelete={handleDelete}
              showRaw
            />
          ))}
        </div>
      )}
    </div>
  );
}
