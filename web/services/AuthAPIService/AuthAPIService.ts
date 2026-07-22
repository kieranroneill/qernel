// services
import BaseAPIService, { type BaseAPIServiceOptions } from '@/services/BaseAPIService';

// types
import type { RequestOptions } from '@/services/BaseAPIService';
import type { GitHubAuthCompleteRequestBody, GitHubAuthStartResponseBody } from '@/types/auth';

export default class AuthAPIService extends BaseAPIService {
  // public
  public static displayName = 'AuthAPIService';

  public constructor(options: BaseAPIServiceOptions = {}) {
    super(options);

    this.routePrefix = '/api/auth';
  }

  /**
   * public methods
   */

  public async completeGitHubAuth(body: GitHubAuthCompleteRequestBody, options?: RequestOptions): Promise<void> {
    const __functionName = 'completeGitHubAuth';
    const logPrefix = `${AuthAPIService.displayName}#${__functionName}`;
    let response: Response;

    try {
      response = await fetch(`${this.routePrefix}/github/callback`, {
        body: JSON.stringify(body),
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'POST',
        ...(options?.signal && {
          signal: options.signal,
        }),
      });

      this._checkHTTPError(response, { logPrefix });
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix });
    }
  }

  public async logout(options?: RequestOptions): Promise<void> {
    const __functionName = 'logout';
    const logPrefix = `${AuthAPIService.displayName}#${__functionName}`;
    let response: Response;

    try {
      response = await fetch(`${this.routePrefix}/logout`, {
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'GET',
        ...(options?.signal && {
          signal: options.signal,
        }),
      });

      this._checkHTTPError(response, { logPrefix });
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix });
    }
  }

  public async startGitHubAuth(options?: RequestOptions): Promise<GitHubAuthStartResponseBody> {
    const __functionName = 'startGitHubAuth';
    const logPrefix = `${AuthAPIService.displayName}#${__functionName}`;
    let response: Response;

    try {
      response = await fetch(`${this.routePrefix}/github/start`, {
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'POST',
        ...(options?.signal && {
          signal: options.signal,
        }),
      });

      this._checkHTTPError(response, { logPrefix });

      return (await response.json()) as Promise<GitHubAuthStartResponseBody>;
    } catch (error) {
      throw this._parseError(error as Error, { logPrefix });
    }
  }
}
