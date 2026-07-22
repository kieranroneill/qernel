import type { ComponentProps } from 'react';

interface Props extends ComponentProps<'div'> {
  size?: 'default' | 'sm';
}

export default Props;
