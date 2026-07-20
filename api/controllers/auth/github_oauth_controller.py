from uuid import uuid4

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.dtos.auth import GitHubOAuthConfigDTO, GitHubOAuthHandshakeDTO
from api.dtos.users import GitHubUserDTO, UserDTO
from api.errors.auth import (
    UnauthorizedError,
)
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.users import FailedToUpdateUserError
from api.repositories.auth import GitHubOAuthHandshakeRepository
from api.repositories.users import UserRepository
from api.services.auth import GitHubOAuthService
from api.utilities.datetime import now
from api.utilities.logging import get_logger


class GitHubOAuthController:
    def __init__(self, database: AsyncSession, github_oauth_config: GitHubOAuthConfigDTO, session_store: Redis) -> None:
        logger = get_logger()

        self._logger = logger
        self._handshake_repository = GitHubOAuthHandshakeRepository(logger=logger, session_store=session_store)
        self._service = GitHubOAuthService(github_oauth_config=github_oauth_config)
        self._user_repository = UserRepository(database=database, logger=logger)

    ##
    # private methods
    ##

    ##
    # public methods
    ##
    async def complete(self, code: str, handshake_id: str, state: str) -> tuple[UserDTO, bool]:
        handshake = await self._handshake_repository.get_by_id(handshake_id)

        if not handshake:
            self._logger.error("no github oauth handshake found in session store")

            raise UnauthorizedError()

        try:
            access_token = await self._service.generate_access_token(
                code=code,
                code_verifier=handshake.code_verifier,
            )
            profile = await self._service.fetch_profile(access_token)
            email = profile.email

            if email is None:
                emails = await self._service.fetch_emails(access_token)
                email = self._service.resolve_primary_email(emails)

            user = await self._user_repository.get_by_email(email)
            _now = now()

            if user is None:
                return (
                    await self._user_repository.add(
                        UserDTO(
                            active=True,
                            created_at=_now,
                            display_name=profile.name,
                            email=email,
                            github=GitHubUserDTO(
                                created_at=_now,
                                id=profile.id,
                                updated_at=_now,
                                username=profile.login,
                            ),
                            id=uuid4(),
                            updated_at=_now,
                        )
                    ),
                    True,
                )

            user.github = GitHubUserDTO(
                created_at=user.github.created_at if user.github is not None else _now,
                id=profile.id,
                updated_at=_now,
                username=profile.login,
            )

            _user = await self._user_repository.update(user)

            if _user is None:
                self._logger.error(f'failed to update user "{user.id}"')

                raise FailedToUpdateUserError(user_id=str(user.id))

            await self._handshake_repository.delete_by_id(handshake_id)

            return _user, False
        except BaseError as e:
            raise e
        except ValueError:
            raise UnauthorizedError()
        except Exception as e:
            self._logger.error(e)

            raise InternalServerError()

    async def start(self, next_path: str = "/app") -> tuple[GitHubOAuthHandshakeDTO, str]:
        # save the handshake to the session store
        handshake = await self._handshake_repository.add(
            GitHubOAuthHandshakeDTO(
                created_at=now(),
                code_verifier=GitHubOAuthService.generate_code_verifier(),
                id=str(uuid4()),
                next_path=next_path,
                state=GitHubOAuthService.generate_state(),
            )
        )
        authorize_url = self._service.generate_authorize_url(
            code_verifier=handshake.code_verifier,
            state=handshake.state,
        )

        return handshake, authorize_url
