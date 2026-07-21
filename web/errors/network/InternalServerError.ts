// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import BaseError from '../_base/BaseError';

export default class InternalServerError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.InternalServerError;
  public readonly displayName: string = 'InternalServerError';
}
