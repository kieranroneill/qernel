from api.schemas.defaults import BaseSchema


class AuthGitHubStartResponseBodySchema(BaseSchema):
    authorize_url: str
