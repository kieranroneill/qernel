'use client';
import { createContext } from 'react';
import type { StoreApi } from 'zustand';

// types
import type { Store } from '@/types/store';

const StoreContext = createContext<StoreApi<Store> | null>(null);

export default StoreContext;
