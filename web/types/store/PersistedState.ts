// types
import type Store from './Store';

type PersistedState = Pick<Store, 'appearanceSettings' | 'sidebarOpen'>;

export default PersistedState;
