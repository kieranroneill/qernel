import { Button as ButtonPrimitive } from '@base-ui/react/button';
import type { FC } from 'react';

// types
import type { Props } from './types';

// utilities
import { createButtonVariants } from './utilities';
import { cn } from '@/utilities/styles';

const Button: FC<Props> = ({ className, variant = 'default', size = 'default', ...props }) => {
  return (
    <ButtonPrimitive
      className={cn(createButtonVariants({ variant, size, className }), 'cursor-pointer')}
      data-slot="button"
      {...props}
    />
  );
};

export default Button;
