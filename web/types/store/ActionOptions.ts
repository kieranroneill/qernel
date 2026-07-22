// types
import type ActionAPI from './ActionAPI';
import type { Logger } from '@/types/logging';

interface ActionOptions {
  api: ActionAPI;
  logger: Logger;
}

export default ActionOptions;
