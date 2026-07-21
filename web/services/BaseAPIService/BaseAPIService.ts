// enums
import { LogLevelEnum } from '@/enums/logging';

// errors
import { BaseError } from '@/errors/_base';
import { InternalServerError, ParsingError } from '@/errors/network';

// types
import type { BaseAPIServiceOptions, ParseErrorOptions } from './types';
import type { Logger } from '@/types/logging';

// utilities
import { createLogger } from '@/utilities/logging';
import { ForbiddenError, UnauthorizedError } from '@/errors';

export default abstract class BaseAPIService {
  // protected
  protected _logger: Logger;
  // public
  public routePrefix: string = '';

  public constructor({ logger }: BaseAPIServiceOptions = {}) {
    this._logger = logger ?? createLogger((process.env.NEXT_PUBLIC_LOG_LEVEL as LogLevelEnum) ?? LogLevelEnum.Error);
  }

  protected _checkHTTPError(response: Response, { logPrefix }: ParseErrorOptions): void {
    let error: string;

    if (!response.ok) {
      error = `failed to get response - ${response.status}`;

      this._logger.error(`${logPrefix}: ${error}`);

      switch (response.status) {
        case 401:
          throw new UnauthorizedError('unauthorized');
        case 403:
          throw new ForbiddenError('forbidden');
        default:
          throw new InternalServerError(error);
      }
    }

    return;
  }

  protected _parseError(error: Error, { logPrefix }: ParseErrorOptions): BaseError {
    if ((error as BaseError).isQernelError()) {
      return error as BaseError;
    }

    this._logger.error(`${logPrefix}:`, error);

    if (error instanceof TypeError || error instanceof SyntaxError) {
      return new ParsingError(`failed to parse response`);
    }

    return new InternalServerError(error.message);
  }
}
