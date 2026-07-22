// errors
import type { BaseError } from '@/errors/_base';

// services
import AuthAPIService from '@/services/AuthAPIService';

// types
import type { GitHubAuthStartResponseBody } from '@/types/auth';
import type { ActionOptions } from '@/types/store';

export default function startGitHubOAuthAction({
  api,
  logger,
}: ActionOptions): () => Promise<GitHubAuthStartResponseBody> {
  return async () => {
    const __functionName = 'startGitHubOAuthAction';
    const apiService = new AuthAPIService({
      logger,
    });
    let result: GitHubAuthStartResponseBody;

    api.setState((state) => ({
      ...state,
      authenticating: true,
    }));

    try {
      result = await apiService.startGitHubAuth();

      logger.debug(`${__functionName}:`, result);

      api.setState((state) => ({
        ...state,
        githubOAuthHandshake: {
          authorizeUrl: result.authorizeUrl,
        },
      }));

      return result;
    } catch (error) {
      api.setState((state) => ({
        ...state,
        authenticating: false,
        authenticationError: error as BaseError,
      }));

      throw error;
    }
  };
}
