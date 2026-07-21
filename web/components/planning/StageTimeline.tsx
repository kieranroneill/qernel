import React from 'react';
import type { BuildStage, TimelineEvent } from '@/types';
import { STAGE_ORDER, STAGE_CONFIG } from '@/constants/stages';
import { CheckCircle2, Circle } from 'lucide-react';

interface StageTimelineProps {
  currentStage: BuildStage;
  events?: TimelineEvent[];
}

export function StageTimeline({ currentStage, events = [] }: StageTimelineProps) {
  const currentStageIndex = STAGE_ORDER.indexOf(currentStage);

  return (
    <div className="flex items-center justify-between gap-2">
      {STAGE_ORDER.map((stage, index) => {
        const isComplete = index < currentStageIndex;
        const isCurrent = index === currentStageIndex;
        const config = STAGE_CONFIG[stage];

        return (
          <div key={stage} className="flex items-center flex-1">
            {/* Stage Circle */}
            <div className="relative flex items-center justify-center">
              <div
                className={`flex h-10 w-10 items-center justify-center rounded-full border-2 transition-colors ${
                  isComplete
                    ? 'border-primary bg-primary'
                    : isCurrent
                      ? 'border-primary bg-background'
                      : 'border-muted bg-muted/30'
                }`}
              >
                {isComplete ? (
                  <CheckCircle2 size={20} className="text-primary-foreground" />
                ) : isCurrent ? (
                  <Circle size={20} className="text-primary" />
                ) : (
                  <Circle size={20} className="text-muted-foreground" />
                )}
              </div>
              <div className="absolute top-full mt-2 text-center">
                <p className={`text-xs font-medium ${isCurrent ? 'text-foreground' : 'text-muted-foreground'}`}>
                  {config.label}
                </p>
              </div>
            </div>

            {/* Connector Line */}
            {index < STAGE_ORDER.length - 1 && (
              <div className="mx-1 flex-1">
                <div className={`h-1 rounded transition-colors ${isComplete ? 'bg-primary' : 'bg-muted/30'}`} />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
