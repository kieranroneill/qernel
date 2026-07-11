from fastapi import HTTPException

from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class ModelNotSupportedError(BaseError):
    def __init__(self, message: str | None = None, provider: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.MODEL_NOT_SUPPORTED_ERROR, message or "Model Not Supported")

        self.provider = provider

    def to_http_exception(self, status_code: int) -> HTTPException:
        return HTTPException(
            detail={
                "code": self.code,
                "message": self.message,
                "provider": self.provider,
            },
            status_code=status_code,
        )
