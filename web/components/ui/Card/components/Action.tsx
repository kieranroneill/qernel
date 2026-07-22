'use client';
import { type FC } from 'react';

// types
import type { ActionProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Action: FC<Props> = ({ className, ...props }) => {
  return (
    <div
      className={cn('col-start-2 row-span-2 row-start-1 self-start justify-self-end', className)}
      data-slot="card-action"
      {...props}
    />
  );
};

export default Action;
