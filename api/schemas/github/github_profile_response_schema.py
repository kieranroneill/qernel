from api.schemas.defaults import BaseSchema


class GitHubProfileResponseSchema(BaseSchema):
    email: str | None
    id: int
    login: str
    name: str
