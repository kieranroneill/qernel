from api.schemas.defaults import BaseSchema


class GitHubEmailResponseSchema(BaseSchema):
    email: str
    primary: bool
    verified: bool
    visibility: str
