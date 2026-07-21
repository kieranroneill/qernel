// types
import type Email from './Email';
import type GitHubUser from './GitHubUser';

interface User {
  active: boolean;
  createdAt: string;
  displayName: string;
  emails: Email[];
  github: GitHubUser | null;
  id: string;
  primaryEmail: Email | null;
  updatedAt: string;
}

export default User;
