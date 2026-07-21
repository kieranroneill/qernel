// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import BaseError from '../_base/BaseError';

export default class ParsingError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.MalformedDataError;
  public readonly displayName: string = 'MalformedDataError';
}
