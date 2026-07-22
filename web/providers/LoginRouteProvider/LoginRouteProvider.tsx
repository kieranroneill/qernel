'use client';

import { useRouter } from 'next/navigation';
import { type FC, type PropsWithChildren, useEffect } from 'react';

// hooks
import useStore from '@/hooks/useStore';

const LoginRouteProvider: FC<PropsWithChildren> = ({ children }) => {
  const router = useRouter();
  // hooks
  const meAction = useStore(({ meAction }) => meAction);
  const user = useStore(({ user }) => user);

  // if there is no user data
  useEffect(() => void meAction(), [router]);
  useEffect(() => {
    if (user) {
      router.push('/dashboard');
    }
  }, [user]);

  return children;
};

LoginRouteProvider.displayName = 'LoginRouteProvider';

export default LoginRouteProvider;
