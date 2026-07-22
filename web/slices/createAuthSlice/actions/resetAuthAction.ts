// types
import type { ActionOptions } from '@/types/store';

export default function resetAuthAction({ api, logger }: ActionOptions): () => void {
  return () => {
    const __functionName = 'resetAuthAction';

    logger.debug(`${__functionName}: resetting auth`);

    api.setState((state) => ({
      ...state,
      authenticating: false,
      authenticationError: null,
      githubOAuthHandshake: null,
    }));
  };
}
