// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import BaseError from '../_base/BaseError';

export default class UnknownError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.UnknownError;
  public readonly displayName: string = 'UnknownError';
}
