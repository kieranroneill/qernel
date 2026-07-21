// enums
import { ErrorCodeEnum } from '@/enums/common';

export default abstract class BaseError extends Error {
  // private
  private readonly __isQernelError = true;
  // public
  public readonly code: ErrorCodeEnum;
  public readonly displayName: string;
  public message: string;

  public constructor(message: string) {
    super(message.toLowerCase());
  }

  public isQernelError(): boolean {
    return this.__isQernelError;
  }
}
