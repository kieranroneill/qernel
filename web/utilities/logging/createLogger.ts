// enums
import { LogLevelEnum } from '@/enums/logging';

// types
import type { Logger } from '@/types/logging';

/**
 * Creates a logger that can set whether the logs appear based on the level.
 * @param {LogLevelEnum} level - The base level of logging.
 * @returns {Logger} A logger that can be used to create logs based on the level.
 */
export default function createLogger(level: LogLevelEnum = LogLevelEnum.Error): Logger {
  const canLog: (allowedLevel: LogLevelEnum) => boolean = (allowedLevel): boolean => {
    switch (level) {
      case LogLevelEnum.Error:
        return allowedLevel === LogLevelEnum.Error;
      case LogLevelEnum.Warn:
        return allowedLevel === LogLevelEnum.Error || allowedLevel === LogLevelEnum.Warn;
      case LogLevelEnum.Info:
        return (
          allowedLevel === LogLevelEnum.Error ||
          allowedLevel === LogLevelEnum.Warn ||
          allowedLevel === LogLevelEnum.Info
        );
      case LogLevelEnum.Debug:
        return true;
      default:
        return false;
    }
  };

  return {
    /* eslint-disable @typescript-eslint/no-explicit-any */
    debug: (message: any, ...optionalParams: any[]) =>
      canLog(LogLevelEnum.Debug) && console.log(`\x1b[34m[DEBUG]\x1b[0m ${message}`, ...optionalParams),
    error: (message: any, ...optionalParams: any[]) =>
      canLog(LogLevelEnum.Error) && console.log(`\x1b[31m[ERROR]\x1b[0m ${message}`, ...optionalParams),
    info: (message: any, ...optionalParams: any[]) =>
      canLog(LogLevelEnum.Info) && console.log(`\x1b[37m[INFO]\x1b[0m ${message}`, ...optionalParams),
    success: (message: any, ...optionalParams: any[]) =>
      canLog(LogLevelEnum.Info) && console.log(`\x1b[32m[SUCCESS]\x1b[0m ${message}`, ...optionalParams),
    warn: (message: any, ...optionalParams: any[]) =>
      canLog(LogLevelEnum.Warn) && console.log(`\x1b[33m[WARN]\x1b[0m ${message}`, ...optionalParams),
    /* eslint-enable @typescript-eslint/no-explicit-any */
  };
}
