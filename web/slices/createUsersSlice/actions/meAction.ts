// services
import UsersAPIService from '@/services/UsersAPIService';

// types
import type { BaseError } from '@/errors/_base';
import type { ActionOptions } from '@/types/store';
import type { User } from '@/types/users';

export default function meAction({ api, logger }: ActionOptions): () => Promise<void> {
  return async () => {
    const __functionName = 'meAction';
    const apiService = new UsersAPIService({
      logger,
    });
    let result: User;

    api.setState((state) => ({
      ...state,
      fetchingUser: true,
    }));

    try {
      result = await apiService.me();

      logger.debug(`${__functionName}:`, result);

      api.setState((state) => ({
        ...state,
        user: result,
      }));
    } catch (error) {
      api.setState((state) => ({
        ...state,
        fetchingUser: false,
        fetchUserError: error as BaseError,
      }));
    }
  };
}
