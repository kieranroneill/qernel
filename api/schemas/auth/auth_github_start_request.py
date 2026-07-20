from api.schemas.defaults import BaseSchema


class AuthGitHubStartRequest(BaseSchema):
    next_path: str | None = "/app"
