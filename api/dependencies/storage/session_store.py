from fastapi import Request
from redis.asyncio import Redis


def session_store(request: Request) -> Redis:
    """Return the Redis session store attached to the application.

    Args:
        request (Request): The current FastAPI request.

    Returns:
        Redis: The Redis session store configured on the application.
    """
    return request.app.state.session_store
