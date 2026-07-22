import { Button as ButtonPrimitive } from '@base-ui/react/button';
import type { VariantProps } from 'class-variance-authority';

// utilities
import { createButtonVariants } from '../utilities';

type Props = ButtonPrimitive.Props & VariantProps<typeof createButtonVariants>;

export default Props;
