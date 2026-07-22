import type { FC } from 'react';

// types
import ActionProps from './ActionProps';
import ContentProps from './ContentProps';
import DescriptionProps from './DescriptionProps';
import FooterProps from './FooterProps';
import HeaderProps from './HeaderProps';
import TitleProps from './TitleProps';

interface Component<Props> extends FC<Props> {
  Action: FC<ActionProps>;
  Content: FC<ContentProps>;
  Description: FC<DescriptionProps>;
  Footer: FC<FooterProps>;
  Header: FC<HeaderProps>;
  Title: FC<TitleProps>;
}

export default Component;
