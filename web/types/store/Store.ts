// types
import type { Slice as AuthSlice } from '@/slices/createAuthSlice';
import type { Slice as SettingsSlice } from '@/slices/createSettingsSlice';
import type { Slice as SystemSlice } from '@/slices/createSystemSlice';
import type { Slice as UsersSlice } from '@/slices/createUsersSlice';

type Store = AuthSlice & SettingsSlice & SystemSlice & UsersSlice;

export default Store;
