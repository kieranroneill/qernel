from api.constants import AUTH_TRANSACTION_TTL_SECONDS
from api.dtos.auth import AuthTransactionDTO
from api.repositories.defaults import BaseSessionRepository


class AuthTransactionRepository(BaseSessionRepository[AuthTransactionDTO]):
    ##
    # private methods
    ##
    def _key(self, _id: str) -> str:
        return f"auth_transaction:{_id}"

    ##
    # public methods
    ##
    async def add(self, dto: AuthTransactionDTO) -> AuthTransactionDTO:
        key = self._key(dto.id)

        await self._session_store.hset(
            key,
            mapping=dto.to_dict(),
        )

        # add a ttl to delete after a ste time
        await self._session_store.expire(key, AUTH_TRANSACTION_TTL_SECONDS)

        self._logger.debug('added "%s"', key)

        return dto

    async def get_by_id(self, _id: str) -> AuthTransactionDTO | None:
        result = await self._session_store.hgetall(self._key(_id))

        if not result:
            return None

        return AuthTransactionDTO.from_dict(result)
