from fastapi import Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.controllers.auth import GitHubOAuthController
from api.dependencies.storage import database, session_store


async def github_oauth_controller(
    request: Request, _database: AsyncSession = Depends(database), _session_store: Redis = Depends(session_store)
) -> GitHubOAuthController:
    return GitHubOAuthController(
        database=_database,
        github_oauth_config=request.app.state.config.auth.github,
        session_store=_session_store,
    )
