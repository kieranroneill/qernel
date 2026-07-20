from api.constants import GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS
from api.dtos.auth import GitHubOAuthHandshakeDTO
from api.repositories.defaults import BaseSessionRepository


class GitHubOAuthHandshakeRepository(BaseSessionRepository[GitHubOAuthHandshakeDTO]):
    ##
    # private methods
    ##
    def _key(self, _id: str) -> str:
        return f"github_oauth_handshake:{_id}"

    ##
    # public methods
    ##
    async def add(self, dto: GitHubOAuthHandshakeDTO) -> GitHubOAuthHandshakeDTO:
        key = self._key(dto.id)

        await self._session_store.hset(
            key,
            mapping=dto.to_dict(),
        )

        # add a ttl to delete after a ste time
        await self._session_store.expire(key, GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS)

        self._logger.debug('added "%s"', key)

        return dto

    async def get_by_id(self, _id: str) -> GitHubOAuthHandshakeDTO | None:
        result = await self._session_store.hgetall(self._key(_id))

        if not result:
            return None

        return GitHubOAuthHandshakeDTO.from_dict(result)
