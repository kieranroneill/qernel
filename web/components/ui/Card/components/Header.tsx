'use client';
import { type FC } from 'react';

// types
import type { HeaderProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Header: FC<Props> = ({ className, ...props }) => {
  return <div data-slot="sheet-header" className={cn('flex flex-col gap-0.5 p-4', className)} {...props} />;
};

export default Header;
