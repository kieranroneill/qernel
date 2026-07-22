'use client';

import { useT } from 'next-i18next/client';
import { type FC, type PropsWithChildren, useEffect } from 'react';

// hooks
import useStore from '@/hooks/useStore';

// selectors
import { useLogger } from '@/selectors/logging';
import { useRouter } from 'next/navigation';

const AuthenticatedRouteProvider: FC<PropsWithChildren> = ({ children }) => {
  const { t } = useT();
  const router = useRouter();
  // selectors
  const logger = useLogger();
  // hooks
  const authenticationError = useStore(({ authenticationError }) => authenticationError);
  const authenticating = useStore(({ authenticating }) => authenticating);
  const fetchingUser = useStore(({ fetchingUser }) => fetchingUser);
  const user = useStore(({ user }) => user);

  // if there is no user data
  useEffect(() => {
    if (!fetchingUser && !user) {
      logger.debug(`${AuthenticatedRouteProvider.displayName}#useEffect: no user data, redirecting to login`);

      router.push('/login');
    }
  }, [fetchingUser, user]);
  // if there is an authentication error
  useEffect(() => {
    if (!authenticating && authenticationError) {
      logger.debug(
        `${AuthenticatedRouteProvider.displayName}#useEffect: authentication error "${authenticationError.code}", redirecting to login`
      );
      router.push('/login');
    }
  }, [authenticating, authenticationError, router]);

  if (authenticating || fetchingUser) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />

          <p className="text-sm text-muted-foreground">{t('common:captions.loading')}</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return children;
};

AuthenticatedRouteProvider.displayName = 'AuthenticatedRouteProvider';

export default AuthenticatedRouteProvider;
