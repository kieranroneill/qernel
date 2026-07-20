from fastapi import HTTPException

from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class FailedToUpdateUserError(BaseError):
    def __init__(self, message: str | None = None, user_id: str | None = None) -> None:
        _message = "failed to update user"

        if user_id:
            _message = f'{message} "{user_id}"'

        super().__init__(ErrorCodeEnum.FAILED_TO_UPDATE_USER_ERROR, message or _message)

        self.user_id = user_id

    def to_http_exception(self, status_code: int) -> HTTPException:
        return HTTPException(
            detail={
                "code": self.code.value,
                "message": self.message,
                "user_id": self.user_id,
            },
            status_code=status_code,
        )
