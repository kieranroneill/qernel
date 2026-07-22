// types
import type ActionAPI from './ActionAPI';

type ActionCreator<Payload = undefined, Return = void> = (api: ActionAPI) => (payload: Payload) => Return;

export default ActionCreator;
