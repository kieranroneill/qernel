from fastapi import Request

from api.dtos.auth import AuthContextDTO


def auth_context(request: Request) -> AuthContextDTO | None:
    """Return the auth context stored on the current request state.

    Args:
        request (Request): The current FastAPI request.

    Returns:
        AuthContextDTO | None: The auth context stored on the request state, or ``None`` if absent.
    """
    return request.state.auth_context
