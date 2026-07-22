import React, { ReactNode } from 'react';
import { Card } from '@/components/ui/card';
import { AlertCircle } from 'lucide-react';

// components
import Button from '@/components/ui/Button';

interface ErrorStateProps {
  title: string;
  message: string;
  onRetry?: () => void;
  action?: ReactNode;
}

export function ErrorState({ title, message, onRetry, action }: ErrorStateProps) {
  return (
    <div className="p-6 md:p-8">
      <Card className="border-destructive/20 bg-destructive/5">
        <div className="flex gap-4 p-6">
          <AlertCircle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="font-medium text-destructive">{title}</h3>
            <p className="mt-2 text-sm text-destructive/80">{message}</p>
            <div className="mt-4 flex gap-2">
              {onRetry && (
                <Button onClick={onRetry} variant="outline" size="sm">
                  Try Again
                </Button>
              )}
              {action}
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
