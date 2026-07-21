import React from 'react';
import type { BuildStage } from '@/types';
import { STAGE_CONFIG } from '@/constants/stages';

interface StageBadgeProps {
  stage: BuildStage;
  size?: 'sm' | 'md';
}

export function StageBadge({ stage, size = 'sm' }: StageBadgeProps) {
  const config = STAGE_CONFIG[stage];

  const sizeClasses = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1.5',
  };

  return (
    <span className={`inline-flex items-center rounded-full font-medium ${config.color} ${sizeClasses[size]}`}>
      {config.label}
    </span>
  );
}
