// types
import type { ActionOptions } from '@/types/store';

export default function setSidebarAction({ api }: ActionOptions): (open: boolean) => void {
  return (open: boolean) => {
    api.setState((state) => ({
      ...state,
      sidebarOpen: open,
    }));
  };
}
