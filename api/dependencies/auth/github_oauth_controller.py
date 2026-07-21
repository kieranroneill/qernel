from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.controllers.auth import GitHubOAuthController
from api.dependencies.storage import database, session_store


async def github_oauth_controller(
    request: Request, _database: AsyncSession = Depends(database), _session_store: Redis = Depends(session_store)
) -> GitHubOAuthController:
    """Build a GitHub OAuth controller for the current application context.

    Args:
        request (Request): The current FastAPI request.
        _database (AsyncSession): The database session for the current request.
        _session_store (Redis): The Redis session store for the current request.

    Returns:
        GitHubOAuthController: A configured GitHub OAuth controller.
    """
    return GitHubOAuthController(
        database=_database,
        github_oauth_config=request.app.state.config.auth.github,
        session_store=_session_store,
    )
