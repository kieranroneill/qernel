// types
import type { AppearanceSettings } from '../types';
import type { ColorScheme } from '@/types/settings';

interface Slice {
  // actions
  setColorSchemeAction: (colorScheme: ColorScheme) => void;
  // state
  appearanceSettings: AppearanceSettings;
}

export default Slice;
