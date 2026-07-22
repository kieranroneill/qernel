// actions
import { resetAuthAction, startGitHubOAuthAction } from './actions';

// types
import type { ActionOptions, SliceOptions, StateCreator } from '@/types/store';
import type { Slice } from './types';

const createAuthSlice: (options: SliceOptions) => StateCreator<Slice> =
  ({ logger }) =>
  (setState, getState) => {
    const actionOptions: ActionOptions = {
      api: { getState, setState },
      logger,
    };

    return {
      // actions
      resetAuthAction: resetAuthAction(actionOptions),
      startGitHubOAuthAction: startGitHubOAuthAction(actionOptions),
      // state
      authenticating: false,
      authenticationError: null,
      githubOAuthHandshake: null,
    };
  };

export default createAuthSlice;
