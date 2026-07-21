// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import { BaseError } from '@/errors/_base';

export default class UnauthorizedError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.UnauthorizedError;
  public readonly displayName: string = 'UnauthorizedError';
}
