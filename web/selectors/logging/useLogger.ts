'use client';
// enums
import { LogLevelEnum } from '@/enums/logging';

// types
import type { Logger } from '@/types/logging';

// utilities
import { createLogger } from '@/utilities/logging';

export default function useLogger(): Logger {
  return createLogger((process.env.NEXT_PUBLIC_LOG_LEVEL as LogLevelEnum) ?? LogLevelEnum.Error);
}
