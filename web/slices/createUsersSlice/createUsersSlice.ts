// actions
import { meAction } from './actions';

// types
import type { ActionOptions, SliceOptions, StateCreator } from '@/types/store';
import type { Slice } from './types';

const createUsersSlice: (options: SliceOptions) => StateCreator<Slice> =
  ({ logger }) =>
  (setState, getState) => {
    const actionOptions: ActionOptions = {
      api: { getState, setState },
      logger,
    };

    return {
      // actions
      meAction: meAction(actionOptions),
      // state
      fetchingUser: false,
      fetchUserError: null,
      user: null,
    };
  };

export default createUsersSlice;
