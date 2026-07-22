'use client';
import { devtools, persist, type PersistOptions } from 'zustand/middleware';
import { createStore, type StoreApi } from 'zustand/vanilla';

// constants
import { STORE_NAME } from '@/constants';

// enums
import { LogLevelEnum } from '@/enums/logging';

// slices
import createAuthSlice from '@/slices/createAuthSlice';
import createSettingsSlice from '@/slices/createSettingsSlice';
import createSystemSlice from '@/slices/createSystemSlice';
import createUsersSlice from '@/slices/createUsersSlice';

// types
import type { PersistedState, SliceOptions, Store } from '@/types/store';

// utilities
import { createLogger } from '@/utilities/logging';

const store: () => StoreApi<Store> = () => {
  const sliceOptions: SliceOptions = {
    logger: createLogger((process.env.NEXT_PUBLIC_LOG_LEVEL as LogLevelEnum) ?? LogLevelEnum.Error),
  };

  return createStore<Store>()(
    devtools(
      persist(
        (...api) => ({
          ...createAuthSlice(sliceOptions)(...api),
          ...createSettingsSlice(sliceOptions)(...api),
          ...createSystemSlice(sliceOptions)(...api),
          ...createUsersSlice(sliceOptions)(...api),
        }),
        {
          name: STORE_NAME,
          partialize: ({ appearanceSettings, sidebarOpen }) => ({
            appearanceSettings,
            sidebarOpen,
          }),
          version: 0,
        } as PersistOptions<Store, PersistedState>
      ),
      {
        name: STORE_NAME,
      }
    )
  );
};

export default store;
