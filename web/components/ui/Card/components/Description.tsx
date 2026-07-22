'use client';
import { type FC } from 'react';

// types
import type { DescriptionProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Description: FC<Props> = ({ className, ...props }) => {
  return <div className={cn('text-sm text-muted-foreground', className)} data-slot="card-description" {...props} />;
};

export default Description;
