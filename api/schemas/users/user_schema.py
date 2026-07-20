from datetime import datetime
from uuid import UUID

from pydantic import Field

from api.schemas.defaults import BaseSchema
from api.schemas.users import GitHubUserSchema


class UserSchema(BaseSchema):
    active: bool = True
    created_at: datetime
    display_name: str | None = None
    email: str = Field(..., min_length=1)
    github: GitHubUserSchema | None = None
    id: UUID
    updated_at: datetime
