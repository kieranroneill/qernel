// services
import BaseAPIService, { type BaseAPIServiceOptions } from '@/services/BaseAPIService';

// types
import type { RequestOptions } from '@/services/BaseAPIService';
import type { User } from '@/types/users';

export default class UsersAPIService extends BaseAPIService {
  // public
  public static displayName = 'AuthAPIService';

  public constructor(options: BaseAPIServiceOptions = {}) {
    super(options);

    this.routePrefix = '/api/users';
  }

  /**
   * public methods
   */

  public async me(options?: RequestOptions): Promise<User> {
    const __functionName = 'me';
    const logPrefix = `${UsersAPIService.displayName}#${__functionName}`;
    let response: Response;

    try {
      response = await fetch(`${this.routePrefix}/me`, {
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'GET',
        ...(options?.signal && {
          signal: options.signal,
        }),
      });

      this._checkHTTPError(response, { logPrefix });

      return (await response.json()) as User;
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix });
    }
  }
}
