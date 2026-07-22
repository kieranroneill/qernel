import { type FC } from 'react';

// types
import type { ContentProps as Props } from '../types';

// utilities
import { cn } from '@/utilities';

const Content: FC<Props> = ({ className, ...props }) => {
  return <div className={cn('px-(--card-spacing)', className)} data-slot="card-content" {...props} />;
};

export default Content;
