from fastapi import HTTPException

from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class MessageRoleNotSupportedError(BaseError):
    def __init__(self, message: str | None = None, role: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.MESSAGE_ROLE_NOT_SUPPORTED_ERROR, message or "message role not supported")

        self.role = role

    def to_http_exception(self, status_code: int) -> HTTPException:
        return HTTPException(
            detail={
                "code": self.code.value,
                "message": self.message,
                "role": self.role,
            },
            status_code=status_code,
        )
