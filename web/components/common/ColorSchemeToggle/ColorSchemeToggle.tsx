'use client';

import { Moon, Sun, Monitor } from 'lucide-react';
import { type FC, useCallback } from 'react';

// components
import { Button } from '@/components/ui/button';

// hooks
import useStore from '@/hooks/useStore';

// types
import type { Props } from './types';
import type { ColorScheme } from '@/types/settings';

const ColorSchemeToggle: FC<Props> = () => {
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
        title="Light theme"
      >
        <Sun size={16} />
      </Button>

      <Button
        size="sm"
        variant={colorScheme === 'dark' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={handleColorSchemeChange('dark')}
        title="Dark theme"
      >
        <Moon size={16} />
      </Button>

      <Button
        size="sm"
        variant={colorScheme === 'system' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={handleColorSchemeChange('system')}
        title="System theme"
      >
        <Monitor size={16} />
      </Button>
    </div>
  );
};

ColorSchemeToggle.displayName = 'ColorSchemeToggle';

export default ColorSchemeToggle;
