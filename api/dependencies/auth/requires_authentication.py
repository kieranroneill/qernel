from fastapi import Depends, status

from api.dtos.auth import AuthContextDTO

from ...errors.auth import UnauthorizedError
from .auth_context import auth_context


def requires_authentication(
    _auth_context: AuthContextDTO | None = Depends(auth_context),
) -> AuthContextDTO:
    if not _auth_context:
        raise UnauthorizedError().to_http_exception(status_code=status.HTTP_401_UNAUTHORIZED)

    return _auth_context
