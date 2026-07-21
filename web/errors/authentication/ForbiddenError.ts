// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import { BaseError } from '@/errors/_base';

export default class ForbiddenError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.ForbiddenError;
  public readonly displayName: string = 'ForbiddenError';
}
