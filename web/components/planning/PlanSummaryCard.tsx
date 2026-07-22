import React from 'react';
import { Card } from '@/components/ui/card';
import type { Plan } from '@/types';
import { CheckCircle2, Loader2 } from 'lucide-react';

// components
import Button from '@/components/ui/Button';

interface PlanSummaryCardProps {
  plan: Plan;
  onConfirm: () => Promise<void>;
  isConfirming?: boolean;
  isConfirmed?: boolean;
}

export function PlanSummaryCard({ plan, onConfirm, isConfirming = false, isConfirmed = false }: PlanSummaryCardProps) {
  return (
    <Card>
      <div className="space-y-6 p-6">
        {/* Header */}
        <div>
          <h3 className="text-lg font-medium">{plan.title}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{plan.description}</p>
        </div>

        {/* Steps */}
        {plan.steps.length > 0 && (
          <div className="space-y-3 border-t border-border pt-6">
            <h4 className="text-sm font-medium">Implementation Steps</h4>
            <div className="space-y-2">
              {plan.steps
                .sort((a, b) => a.order - b.order)
                .map((step) => (
                  <div key={step.id} className="flex gap-3 rounded-lg bg-muted/30 p-3">
                    <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/20 text-xs font-medium text-primary">
                      {step.order}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{step.title}</p>
                      <p className="text-xs text-muted-foreground">{step.description}</p>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Confirmation Status */}
        {isConfirmed && (
          <div className="flex items-center gap-2 rounded-lg bg-green-50 p-3 dark:bg-green-950">
            <CheckCircle2 size={20} className="text-green-600 dark:text-green-400" />
            <p className="text-sm font-medium text-green-700 dark:text-green-300">
              Plan confirmed and ready for generation
            </p>
          </div>
        )}

        {/* Action Button */}
        {!isConfirmed && (
          <div className="flex justify-end gap-3 border-t border-border pt-6">
            <Button onClick={onConfirm} disabled={isConfirming} size="lg" className="gap-2">
              {isConfirming ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
                  Confirming...
                </>
              ) : (
                'Confirm Plan'
              )}
            </Button>
          </div>
        )}
      </div>
    </Card>
  );
}
