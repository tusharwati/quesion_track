import { HelpCircle } from 'lucide-react';
import { useStore } from '@/hooks/useStore';
import { QuestionCard } from './QuestionCard';
import { questionsApi } from '@/services/api';

export function LatestQuestions() {
  const { recentQuestions, settings, removeQuestion } = useStore();
  
  const handleDelete = async (id: string) => {
    try {
      await questionsApi.delete(parseInt(id));
      removeQuestion(id);
    } catch (error) {
      console.error('Failed to delete question:', error);
    }
  };
  
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Latest Questions
        </h2>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          Showing {recentQuestions.length} of {settings.recent_question_count}
        </span>
      </div>
      
      {recentQuestions.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-gray-400">
          <HelpCircle className="w-12 h-12 mb-2 opacity-50" />
          <p className="text-sm">No questions detected yet</p>
          <p className="text-xs mt-1">Start recording to capture questions</p>
        </div>
      ) : (
        <div className="space-y-3">
          {recentQuestions.map((question, index) => (
            <div key={question.id} className="relative">
              <div className="absolute -left-2 top-4 w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
                <span className="text-xs font-bold text-primary-600 dark:text-primary-400">
                  {index + 1}
                </span>
              </div>
              <div className="pl-6">
                <QuestionCard
                  question={question}
                  onDelete={handleDelete}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
