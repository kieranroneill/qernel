// errors
import type { BaseError } from '@/errors/_base';

// types
import type { GitHubOAuthHandshake } from '../types';

interface Slice {
  // actions
  startGitHubOAuthAction: () => Promise<void>;
  // state
  authenticating: boolean;
  authenticationError: BaseError | null;
  githubOAuthHandshake: GitHubOAuthHandshake | null;
}

export default Slice;
