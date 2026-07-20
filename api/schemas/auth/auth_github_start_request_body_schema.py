from api.schemas.defaults import BaseSchema


class AuthGitHubStartRequestBodySchema(BaseSchema):
    next_path: str = "/app"
