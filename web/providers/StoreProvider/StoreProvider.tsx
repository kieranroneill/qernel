'use client';
import { type FC, type PropsWithChildren, useRef } from 'react';
import { StoreApi } from 'zustand';

// contexts
import { StoreContext } from '@/contexts';

// stores
import createStore from '@/store';

// types
import type { Store } from '@/types/store';

const StoreProvider: FC<PropsWithChildren> = ({ children }) => {
  // refs
  const storeRef = useRef<StoreApi<Store>>(null);

  if (!storeRef.current) {
    storeRef.current = createStore();
  }

  return <StoreContext.Provider value={storeRef.current}>{children}</StoreContext.Provider>;
};

StoreProvider.displayName = 'StoreProvider';

export default StoreProvider;
