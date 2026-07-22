// errors
import type { BaseError } from '@/errors/_base';

// types
import type { GitHubOAuthHandshake } from '../types';
import type { GitHubAuthStartResponseBody } from '@/types/auth';

interface Slice {
  // actions
  resetAuthAction: () => void;
  startGitHubOAuthAction: () => Promise<GitHubAuthStartResponseBody>;
  // state
  authenticating: boolean;
  authenticationError: BaseError | null;
  githubOAuthHandshake: GitHubOAuthHandshake | null;
}

export default Slice;
