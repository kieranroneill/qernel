from api.schemas.defaults import BaseSchema


class AuthGitHubCompleteRequestBodySchema(BaseSchema):
    code: str
    state: str
