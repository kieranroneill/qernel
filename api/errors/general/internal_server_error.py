from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class InternalServerError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.INTERNAL_SERVER_ERROR, message or "Internal server error")
