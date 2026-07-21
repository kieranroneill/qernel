'use client';

import { useEffect, useState } from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';
import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="flex items-center gap-1 rounded-lg border border-input bg-background p-1">
        <div className="h-8 w-8" />
        <div className="h-8 w-8" />
        <div className="h-8 w-8" />
      </div>
    );
  }

  return (
    <div className="flex items-center gap-1 rounded-lg border border-input bg-background p-1">
      <Button
        size="sm"
        variant={theme === 'light' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={() => setTheme('light')}
        title="Light theme"
      >
        <Sun size={16} />
      </Button>
      <Button
        size="sm"
        variant={theme === 'dark' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={() => setTheme('dark')}
        title="Dark theme"
      >
        <Moon size={16} />
      </Button>
      <Button
        size="sm"
        variant={theme === 'system' ? 'default' : 'ghost'}
        className="h-8 w-8 p-0"
        onClick={() => setTheme('system')}
        title="System theme"
      >
        <Monitor size={16} />
      </Button>
    </div>
  );
}
