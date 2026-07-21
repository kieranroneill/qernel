import { useEffect, useMemo, useState } from 'react';

// errors
import type { BaseError } from '@/errors/_base';

// services
import AuthAPIService from '@/services/AuthAPIService';
import UsersAPIService from '@/services/UsersAPIService';

// types
import type { User } from '@/types/users';

export function useAuth() {
  // memos
  const authAPIService = useMemo(() => new AuthAPIService(), []);
  const usersAPIService = useMemo(() => new UsersAPIService(), []);
  // states
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<BaseError | null>(null);

  useEffect(() => {
    void checkAuth();
  }, []);

  async function checkAuth() {
    let _user: User;

    try {
      setLoading(true);

      _user = await usersAPIService.me();

      setUser(_user);
      setError(null);
    } catch (_error) {
      setError(_error as BaseError);
    } finally {
      setLoading(false);
    }
  }

  async function login(code: string, state: string): Promise<void> {
    let _user: User;

    try {
      setLoading(true);
      setError(null);

      await authAPIService.completeGitHubAuth({
        code,
        state,
      });

      _user = await usersAPIService.me();

      setUser(_user);
    } catch (_error) {
      setError(_error as BaseError);
    } finally {
      setLoading(false);
    }
  }

  async function logout() {
    try {
      setLoading(true);

      await authAPIService.logout();

      setUser(null);
    } catch (_error) {
      setError(_error as BaseError);
    } finally {
      setLoading(false);
    }
  }

  return {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };
}
