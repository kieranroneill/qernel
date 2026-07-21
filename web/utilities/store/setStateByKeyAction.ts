// types
import type { ActionOptions, Store } from '@/types/store';

export default function setStateByKeyAction<Payload = undefined>(
  key: keyof Store,
  { api }: ActionOptions
): (payload: Payload) => void {
  return (value) =>
    api.setState((state) => ({
      ...state,
      [key]: value,
    }));
}
