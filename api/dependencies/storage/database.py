from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def database(request: Request) -> AsyncIterator[AsyncSession]:
    """Yield a database session for the active request lifecycle.

    Args:
        request (Request): The current FastAPI request.

    Returns:
        AsyncIterator[AsyncSession]: An asynchronous iterator yielding a database session for the request.
    """
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.database_session_factory

    async with session_factory() as session:
        yield session
