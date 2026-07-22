// types
import type { BaseError } from '@/errors/_base';
import type { User } from '@/types/users';

interface Slice {
  // actions
  meAction: () => Promise<User>;
  // state
  fetchingUser: boolean;
  fetchUserError: BaseError | null;
  user: User | null;
}

export default Slice;
