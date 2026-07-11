from fastapi import HTTPException

from api.enums.system import ErrorCodeEnum


class BaseError(Exception):
    def __init__(self, code: ErrorCodeEnum, message: str) -> None:
        super().__init__(message)

        self.code = code
        self.message = message

    def to_http_exception(self, status_code: int) -> HTTPException:
        return HTTPException(
            detail={
                "code": self.code.value,
                "message": self.message,
            },
            status_code=status_code,
        )
