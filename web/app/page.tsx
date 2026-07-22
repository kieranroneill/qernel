'use client';

import type { NextPage } from 'next';
import { useT } from 'next-i18next/client';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

// hooks
import useStore from '@/hooks/useStore';

const SplashPage: NextPage = () => {
  const { t } = useT();
  const router = useRouter();
  // hooks
  const loading = useStore(({ authenticating, fetchingUser }) => authenticating || fetchingUser);
  const user = useStore(({ user }) => user);

  useEffect(() => {
    if (!loading) {
      if (user) {
        return router.push('/dashboard');
      }

      return router.push('/login');
    }
  }, [loading, router, user]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="flex flex-col items-center space-y-4">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />

        <p className="text-sm text-muted-foreground">{t('common:captions.loading')}</p>
      </div>
    </div>
  );
};

SplashPage.displayName = 'SplashPage';

export default SplashPage;
