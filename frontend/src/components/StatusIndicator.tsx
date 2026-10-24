import { Circle, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { cn } from '@/utils';

interface StatusIndicatorProps {
  status: 'ready' | 'listening' | 'processing' | 'error';
  modelLoaded?: boolean;
}

const statusConfig: Record<
  StatusIndicatorProps['status'],
  {
    icon: typeof CheckCircle;
    label: string;
    className: string;
    bgClassName: string;
    animate?: boolean;
  }
> = {
  ready: {
    icon: CheckCircle,
    label: 'Ready',
    className: 'text-green-600 dark:text-green-400',
    bgClassName: 'bg-green-50 dark:bg-green-900/20',
  },
  listening: {
    icon: Circle,
    label: 'Listening',
    className: 'text-blue-600 dark:text-blue-400',
    bgClassName: 'bg-blue-50 dark:bg-blue-900/20',
  },
  processing: {
    icon: Loader2,
    label: 'Processing',
    className: 'text-yellow-600 dark:text-yellow-400',
    bgClassName: 'bg-yellow-50 dark:bg-yellow-900/20',
    animate: true,
  },
  error: {
    icon: AlertCircle,
    label: 'Error',
    className: 'text-red-600 dark:text-red-400',
    bgClassName: 'bg-red-50 dark:bg-red-900/20',
  },
};

export function StatusIndicator({ status, modelLoaded }: StatusIndicatorProps) {
  const config = statusConfig[status];
  const Icon = config.icon;
  
  return (
    <div
      className={cn(
        'flex items-center gap-2 px-3 py-1.5 rounded-lg',
        config.bgClassName
      )}
      role="status"
      aria-live="polite"
    >
      <Icon
        className={cn(
          'w-4 h-4',
          config.className,
          config.animate && 'animate-spin'
        )}
        aria-hidden="true"
      />
      <span className={cn('text-sm font-medium', config.className)}>
        {config.label}
      </span>
      {modelLoaded !== undefined && (
        <span
          className={cn(
            'text-xs',
            modelLoaded ? 'text-green-600 dark:text-green-400' : 'text-gray-500'
          )}
        >
          {modelLoaded ? 'Model ready' : 'Model loading'}
        </span>
      )}
    </div>
  );
}
