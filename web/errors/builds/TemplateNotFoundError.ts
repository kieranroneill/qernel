// enums
import { ErrorCodeEnum } from '@/enums/common';

// errors
import { BaseError } from '@/errors/_base';

export default class TemplateNotFoundError extends BaseError {
  public readonly code: ErrorCodeEnum = ErrorCodeEnum.TemplateNotFoundError;
  public readonly displayName: string = 'TemplateNotFoundError';
}
