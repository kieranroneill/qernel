// actions
import { setColorSchemeAction } from './actions';

// types
import type { ActionOptions, SliceOptions, StateCreator } from '@/types/store';
import type { Slice } from './types';

const createSettingsSlice: (options: SliceOptions) => StateCreator<Slice> =
  ({ logger }) =>
  (setState, getState) => {
    const actionOptions: ActionOptions = {
      api: { getState, setState },
      logger,
    };

    return {
      // actions
      setColorSchemeAction: setColorSchemeAction(actionOptions),
      // state
      appearanceSettings: {
        colorScheme: 'system',
      },
    };
  };

export default createSettingsSlice;
