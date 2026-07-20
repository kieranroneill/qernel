from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class InvalidGitHubOAuthCookieError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.INVALID_GITHUB_OAUTH_COOKIE_ERROR, message or "invalid github oauth cookie")
