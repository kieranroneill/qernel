from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.constants import SESSION_TTL_SECONDS
from api.dtos.auth import GitHubOAuthConfigDTO, GitHubOAuthHandshakeDTO, SessionDTO
from api.dtos.users import GitHubUserDTO, UserDTO
from api.errors.auth import (
    UnauthorizedError,
)
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.errors.users import FailedToUpdateUserError
from api.repositories.auth import GitHubOAuthHandshakeRepository, SessionRepository
from api.repositories.users import UserRepository
from api.services.auth import GitHubOAuthService
from api.utilities.datetime import now
from api.utilities.logging import get_logger


class GitHubOAuthController:
    """
    Coordinates the GitHub OAuth handshake, user provisioning, and session creation.
    """

    def __init__(self, database: AsyncSession, github_oauth_config: GitHubOAuthConfigDTO, session_store: Redis) -> None:
        logger = get_logger()

        self._logger = logger
        self._handshake_repository = GitHubOAuthHandshakeRepository(logger=logger, session_store=session_store)
        self._service = GitHubOAuthService(github_oauth_config=github_oauth_config)
        self._session_repository = SessionRepository(logger=logger, session_store=session_store)
        self._user_repository = UserRepository(database=database, logger=logger)

    ##
    # private methods
    ##
    async def _create_session_from_user_id(self, user_id: UUID) -> SessionDTO:
        """
        Create a session for the given user.

        Args:
            user_id (UUID): The internal user identifier.

        Returns:
            SessionDTO: The persisted session record.
        """

        _now = now()

        return await self._session_repository.add(
            SessionDTO(
                expires_at=_now + timedelta(seconds=SESSION_TTL_SECONDS),
                id=uuid4(),
                issued_at=_now,
                user_id=user_id,
            )
        )

    ##
    # public methods
    ##
    async def complete(self, code: str, handshake_id: str, state: str) -> tuple[SessionDTO, bool]:
        """
        Completes the GitHub OAuth flow and create or update the local user.

        Args:
            code (str): The authorization code returned by GitHub.
            handshake_id (str): The stored OAuth handshake identifier.
            state (str): The OAuth state value returned by GitHub.

        Returns:
            tuple[SessionDTO, bool]: The created session and a flag indicating whether a new user was created.

        Raises:
            UnauthorizedError: If the handshake is not found or the state does not match.
            FailedToUpdateUserError: If an error occurs while updating the user.
            InternalServerError: If an unexpected error occurs during the process.
        """

        handshake = await self._handshake_repository.get_by_id(handshake_id)

        if not handshake:
            self._logger.error("no github oauth handshake found in session store")

            raise UnauthorizedError()

        if state != handshake.state:
            self._logger.error("github oauth handshake state mismatch")

            raise UnauthorizedError()

        try:
            access_token = await self._service.generate_access_token(
                code=code,
                code_verifier=handshake.code_verifier,
            )
            profile = await self._service.fetch_profile(access_token)
            user = await self._user_repository.get_by_github_id(profile.id)
            _now = now()

            # if no user is found, create a new user
            if user is None:
                _user = await self._user_repository.add(
                    UserDTO(
                        active=True,
                        created_at=_now,
                        display_name=profile.name,
                        emails=[],
                        github=GitHubUserDTO(
                            created_at=_now,
                            id=profile.id,
                            updated_at=_now,
                            username=profile.login,
                        ),
                        id=uuid4(),
                        primary_email=None,
                        updated_at=_now,
                    )
                )
                user_added = True
            # if a user is found, update the github details
            else:
                user.github = GitHubUserDTO(
                    created_at=user.github.created_at if user.github is not None else _now,
                    id=profile.id,
                    updated_at=_now,
                    username=profile.login,
                )
                user.updated_at = _now
                _user = await self._user_repository.update(user)

                if _user is None:
                    self._logger.error(f'failed to update user "{user.id}"')

                    raise FailedToUpdateUserError(user_id=str(user.id))

                user_added = False

            # delete the handshake
            await self._handshake_repository.delete_by_id(handshake_id)

            # create the session and return it along with the user added flag
            return (
                await self._create_session_from_user_id(_user.id),
                user_added,
            )
        except BaseError as e:
            raise e
        except Exception as e:
            self._logger.error(e)

            raise InternalServerError()

    async def start(self) -> tuple[GitHubOAuthHandshakeDTO, str]:
        """
        Starts the GitHub OAuth flow by persisting a handshake and building the authorize URL.

        Returns:
            tuple[GitHubOAuthHandshakeDTO, str]: The stored handshake and the GitHub authorization URL.
        """

        # save the handshake to the session store
        handshake = await self._handshake_repository.add(
            GitHubOAuthHandshakeDTO(
                created_at=now(),
                code_verifier=GitHubOAuthService.generate_code_verifier(),
                id=str(uuid4()),
                state=GitHubOAuthService.generate_state(),
            )
        )
        authorize_url = self._service.generate_authorize_url(
            code_verifier=handshake.code_verifier,
            state=handshake.state,
        )

        return handshake, authorize_url
