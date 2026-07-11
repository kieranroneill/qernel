from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class TemplateNotFoundError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.TEMPLATE_NOT_FOUND_ERROR, message or "Template not found")
