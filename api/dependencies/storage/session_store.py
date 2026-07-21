from fastapi import Request
from redis.asyncio import Redis


def session_store(request: Request) -> Redis:
    return request.app.state.session_store
