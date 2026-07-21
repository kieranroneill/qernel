from datetime import timedelta
from typing import Awaitable, Callable
from uuid import uuid4

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from api.constants import SESSION_COOKIE_NAME, SESSION_TTL_SECONDS
from api.dtos.auth import AuthContextDTO, SessionDTO
from api.repositories.auth import SessionRepository
from api.repositories.users import UserRepository
from api.utilities.datetime import now
from api.utilities.logging import get_logger


class AuthContextMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        database_session_factory: async_sessionmaker[AsyncSession],
        session_store: Redis,
    ):
        super().__init__(app)

        logger = get_logger()
        self._logger = logger
        self._database_session_factory = database_session_factory
        self._session_store = session_store

    @classmethod
    def _delete_session_cookie_with_response(cls, response: Response) -> Response:
        response.delete_cookie(SESSION_COOKIE_NAME)

        return response

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request.state.auth_context = None
        session_id = request.cookies.get(SESSION_COOKIE_NAME)

        if not session_id:
            self._logger.debug("session cookie not found")

            return await call_next(request)

        session_repository = SessionRepository(logger=self._logger, session_store=self._session_store)
        session = await session_repository.get_by_id(session_id)

        if not session:
            self._logger.debug(f'no session found for "{session_id}"')

            # delete the session cookie
            return AuthContextMiddleware._delete_session_cookie_with_response(response=await call_next(request))

        async with self._database_session_factory() as database:
            user_repository = UserRepository(database=database, logger=self._logger)
            user = await user_repository.get_by_id(session.user_id)

            if not user or not user.active:
                self._logger.debug(f'no user found or user is inactive for session "{session_id}"')

                # invalidate the session
                await session_repository.delete_by_id(session_id)

                # delete the session cookie
                return AuthContextMiddleware._delete_session_cookie_with_response(response=await call_next(request))

            _now = now()

            # create a new session
            session = await session_repository.add(
                SessionDTO(
                    expires_at=_now + timedelta(seconds=SESSION_TTL_SECONDS),
                    id=uuid4(),
                    issued_at=_now,
                    user_id=user.id,
                )
            )

            # delete the old session
            await session_repository.delete_by_id(session_id)

            # add the authenticated context to the request
            request.state.auth_context = AuthContextDTO(
                session=session,
                user=user,
            )

            response = await call_next(request)

            # set the new session cookie with the new session id
            response.set_cookie(
                httponly=True,
                key=SESSION_COOKIE_NAME,
                max_age=SESSION_TTL_SECONDS,
                samesite="lax",
                secure=True,
                value=str(session.id),
            )

            return response
