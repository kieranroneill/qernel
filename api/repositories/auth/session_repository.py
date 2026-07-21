from api.constants import SESSION_TTL_SECONDS
from api.dtos.auth import SessionDTO
from api.repositories.defaults import BaseSessionRepository


class SessionRepository(BaseSessionRepository[SessionDTO]):
    ##
    # private methods
    ##
    def _key(self, _id: str) -> str:
        return f"session:{_id}"

    ##
    # public methods
    ##
    async def add(self, dto: SessionDTO) -> SessionDTO:
        key = self._key(dto.id)

        await self._session_store.hset(
            key,
            mapping=dto.to_dict(),
        )

        # add a ttl to delete after the set time
        await self._session_store.expire(key, SESSION_TTL_SECONDS)

        self._logger.debug('added "%s"', key)

        return dto

    async def get_by_id(self, _id: str) -> SessionDTO | None:
        result = await self._session_store.hgetall(self._key(_id))

        if not result:
            return None

        return SessionDTO.from_dict(result)
