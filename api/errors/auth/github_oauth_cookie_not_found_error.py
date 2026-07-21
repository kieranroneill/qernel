from api.enums.system import ErrorCodeEnum
from api.errors.defaults import BaseError


class GitHubOAuthCookieNotFoundError(BaseError):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(ErrorCodeEnum.GITHUB_OAUTH_COOKIE_NOT_FOUND_ERROR, message or "github oauth cookie not found")
