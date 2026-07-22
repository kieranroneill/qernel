'use client';

import { Moon, Sun, Monitor } from 'lucide-react';
import { useT } from 'next-i18next/client';
import { type FC, useCallback } from 'react';

// components
import Button from '@/components/ui/Button';

// hooks
import useStore from '@/hooks/useStore';

// types
import type { Props } from './types';
import type { ColorScheme } from '@/types/settings';

const ColorSchemeToggle: FC<Props> = () => {
  const { t } = useT();
  // hooks
  const colorScheme = useStore(({ appearanceSettings }) => appearanceSettings.colorScheme);
  const setColorSchemeAction = useStore(({ setColorSchemeAction }) => setColorSchemeAction);
  // callbacks
  const handleColorSchemeChange = useCallback(
    (newColorScheme: ColorScheme) => () => setColorSchemeAction(newColorScheme),
    [setColorSchemeAction]
  );

  return (
    <div className="flex items-center gap-1 rounded-lg border border-input bg-background p-1">
      <Button
        size="sm"
        variant={colorScheme === 'light' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={handleColorSchemeChange('light')}
        title={t('common:labels.lightTheme')}
      >
        <Sun size={16} />
      </Button>

      <Button
        size="sm"
        variant={colorScheme === 'dark' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={handleColorSchemeChange('dark')}
        title={t('common:labels.darkTheme')}
      >
        <Moon size={16} />
      </Button>

      <Button
        size="sm"
        variant={colorScheme === 'system' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={handleColorSchemeChange('system')}
        title={t('common:labels.systemTheme')}
      >
        <Monitor size={16} />
      </Button>
    </div>
  );
};

ColorSchemeToggle.displayName = 'ColorSchemeToggle';

export default ColorSchemeToggle;
