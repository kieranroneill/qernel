'use client';

import { type FC, type PropsWithChildren, useCallback, useEffect } from 'react';

// hooks
import useStore from '@/hooks/useStore';

// selectors
import { useLogger } from '@/selectors/logging';

const ColorSchemeProvider: FC<PropsWithChildren> = ({ children }) => {
  // selectors
  const logger = useLogger();
  // hooks
  const colorScheme = useStore(({ appearanceSettings }) => appearanceSettings.colorScheme);
  // callbacks
  const updateColorScheme = useCallback(() => {
    let resolvedColorScheme: 'dark' | 'light';

    switch (colorScheme) {
      case 'dark':
        resolvedColorScheme = 'dark';
        break;
      case 'light':
        resolvedColorScheme = 'light';
        break;
      case 'system':
      default:
        resolvedColorScheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        break;
    }

    logger.debug(
      `${ColorSchemeProvider.displayName}#updateColorScheme: color scheme changed to "${resolvedColorScheme}"`
    );

    if (resolvedColorScheme == 'dark') {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');

      return;
    }

    document.documentElement.classList.remove('dark');
    document.documentElement.classList.add('light');

    return;
  }, [colorScheme]);
  const handleOnChangeEvent = useCallback(() => {
    logger.debug(`${ColorSchemeProvider.displayName}#handleOnChangeEvent: system color scheme changed`);

    if (colorScheme == 'system') {
      updateColorScheme();
    }
  }, [colorScheme, logger, updateColorScheme]);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // add event listener to trigger an update if the color scheme is set to 'system'
    mediaQuery.addEventListener('change', handleOnChangeEvent);

    return () => mediaQuery.removeEventListener('change', handleOnChangeEvent);
  }, []);
  // update the color scheme on color scheme change
  useEffect(() => updateColorScheme(), [colorScheme]);

  return children;
};

ColorSchemeProvider.displayName = 'ColorSchemeProvider';

export default ColorSchemeProvider;
