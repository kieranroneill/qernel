from datetime import datetime

from api.schemas.defaults import BaseSchema


class GitHubUserSchema(BaseSchema):
    created_at: datetime
    id: int
    updated_at: datetime
    username: str
