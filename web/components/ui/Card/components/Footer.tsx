'use client';
import { type FC } from 'react';

// types
import type { FooterProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Footer: FC<Props> = ({ className, ...props }) => {
  return (
    <div
      className={cn('flex items-center rounded-b-xl border-t bg-muted/50 p-(--card-spacing)', className)}
      data-slot="card-footer"
      {...props}
    />
  );
};

export default Footer;
