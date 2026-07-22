// actions
import { setSidebarAction } from './actions';

// types
import type { ActionOptions, SliceOptions, StateCreator } from '@/types/store';
import type { Slice } from './types';

const createSystemSlice: (options: SliceOptions) => StateCreator<Slice> =
  ({ logger }) =>
  (setState, getState) => {
    const actionOptions: ActionOptions = {
      api: { getState, setState },
      logger,
    };

    return {
      // actions
      setSidebarAction: setSidebarAction(actionOptions),
      // state
      sidebarOpen: false,
    };
  };

export default createSystemSlice;
