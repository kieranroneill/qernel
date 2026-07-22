// services
import UsersAPIService from '@/services/UsersAPIService';

// types
import type { BaseError } from '@/errors/_base';
import type { ActionOptions } from '@/types/store';
import type { User } from '@/types/users';
import { ErrorCodeEnum } from '@/enums';

export default function meAction({ api, logger }: ActionOptions): () => Promise<User> {
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

      return result;
    } catch (error) {
      api.setState((state) => ({
        ...state,
        fetchingUser: false,
        ...((error as BaseError).isQernelError() && (error as BaseError).code === ErrorCodeEnum.UnauthorizedError
          ? {
              authenticatedError: error as BaseError,
            }
          : {
              fetchUserError: error as BaseError,
            }),
      }));

      throw error;
    }
  };
}
