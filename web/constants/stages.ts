import type { BuildStage } from '@/types';

export const STAGE_CONFIG: Record<BuildStage, { label: string; description: string; color: string }> = {
  initiated: {
    label: 'Initiated',
    description: 'Prompt captured, processing your request',
    color: 'bg-slate-200 text-slate-800 dark:bg-slate-700 dark:text-slate-200',
  },
  plan: {
    label: 'Planning',
    description: 'Review and refine the generated plan',
    color: 'bg-blue-200 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  },
  validate: {
    label: 'Validating',
    description: 'Plan is being validated',
    color: 'bg-amber-200 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
  },
  ready: {
    label: 'Ready',
    description: 'Plan confirmed and ready for generation',
    color: 'bg-green-200 text-green-800 dark:bg-green-900 dark:text-green-200',
  },
};

export const STAGE_ORDER: BuildStage[] = ['initiated', 'plan', 'validate', 'ready'];
