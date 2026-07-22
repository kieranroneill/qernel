'use client';
import { type FC } from 'react';

// types
import type { TitleProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Title: FC<Props> = ({ className, ...props }) => {
  return (
    <div
      className={cn('font-heading text-base leading-snug font-medium group-data-[size=sm]/card:text-sm', className)}
      data-slot="card-title"
      {...props}
    />
  );
};

export default Title;
