from api.schemas.defaults import BaseSchema


class GitHubProfileResponseSchema(BaseSchema):
    id: int
    login: str
    name: str
