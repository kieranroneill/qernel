from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class UnauthorizedError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.UNAUTHORIZED_ERROR, message or "unauthorized")
