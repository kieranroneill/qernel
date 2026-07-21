from fastapi import Depends, status

from api.dtos.auth import AuthContextDTO

from ...errors.auth import UnauthorizedError
from .auth_context import auth_context


def requires_authentication(
    _auth_context: AuthContextDTO | None = Depends(auth_context),
) -> AuthContextDTO:
    """Require an authenticated request and return its auth context.

    Args:
        _auth_context (AuthContextDTO | None): The auth context resolved from the current request.

    Returns:
        AuthContextDTO: The authenticated request's auth context.

    Raises:
        UnauthorizedError: If the request is not authenticated, i.e., the auth context from the middleware has not been
        resolved.
    """
    if not _auth_context:
        raise UnauthorizedError().to_http_exception(status_code=status.HTTP_401_UNAUTHORIZED)

    return _auth_context
