from api.schemas.defaults import BaseSchema


class AuthGitHubStartResponse(BaseSchema):
    authorize_url: str
