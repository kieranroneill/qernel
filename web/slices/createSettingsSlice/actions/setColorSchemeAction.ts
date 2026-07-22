// types
import type { ColorScheme } from '@/types/settings';
import type { ActionOptions } from '@/types/store';

export default function setColorSchemeAction({ api }: ActionOptions): (colorScheme: ColorScheme) => void {
  return (colorScheme: ColorScheme) => {
    api.setState((state) => ({
      ...state,
      appearanceSettings: {
        ...state.appearanceSettings,
        colorScheme,
      },
    }));
  };
}
