from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class ForbiddenError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.FORBIDDEN_ERROR, message or "forbidden")
