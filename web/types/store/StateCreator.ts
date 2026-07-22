import type { StateCreator as ZustandStateCreator } from 'zustand';

// types
import type Store from './Store';
import type PersistedState from './PersistedState';

type StateCreator<Slice> = ZustandStateCreator<
  Store,
  [['zustand/devtools', never]],
  [['zustand/persist', PersistedState]],
  Slice
>;

export default StateCreator;
