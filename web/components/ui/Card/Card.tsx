'use client';

// components
import Action from './components/Action';
import Content from './components/Content';
import Description from './components/Description';
import Footer from './components/Footer';
import Header from './components/Header';
import Title from './components/Title';

// types
import type { Component, Props } from './types';

// utilities
import { cn } from '@/utilities/styles';

const Card: Component<Props> = ({ className, size = 'default', ...props }) => {
  return (
    <div
      className={cn(
        'group/card flex flex-col gap-(--card-spacing) overflow-hidden rounded-xl bg-card py-(--card-spacing) text-sm text-card-foreground ring-1 ring-foreground/10 [--card-spacing:--spacing(4)] has-data-[slot=card-footer]:pb-0 has-[>img:first-child]:pt-0 data-[size=sm]:[--card-spacing:--spacing(3)] data-[size=sm]:has-data-[slot=card-footer]:pb-0 *:[img:first-child]:rounded-t-xl *:[img:last-child]:rounded-b-xl',
        className
      )}
      data-size={size}
      data-slot="card"
      {...props}
    />
  );
};

Card.displayName = 'Card';
Card.Action = Action;
Card.Content = Content;
Card.Description = Description;
Card.Footer = Footer;
Card.Header = Header;
Card.Title = Title;

export default Card;
