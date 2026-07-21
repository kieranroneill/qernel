import React, { ReactNode } from 'react';
import { Card } from '@/components/ui/card';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex h-full items-center justify-center p-6 md:p-8">
      <Card className="max-w-md text-center">
        <div className="space-y-4 p-6">
          {icon && <div className="flex justify-center text-muted-foreground">{icon}</div>}
          <h3 className="text-lg font-medium">{title}</h3>
          {description && <p className="text-sm text-muted-foreground">{description}</p>}
          {action && <div className="pt-4">{action}</div>}
        </div>
      </Card>
    </div>
  );
}
