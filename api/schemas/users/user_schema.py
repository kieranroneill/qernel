from datetime import datetime
from uuid import UUID

from pydantic import Field

from api.schemas.defaults import BaseSchema
from api.schemas.users import EmailSchema, GitHubUserSchema


class UserSchema(BaseSchema):
    active: bool = True
    created_at: datetime
    display_name: str | None = None
    emails: list[EmailSchema] = Field(default_factory=list)
    github: GitHubUserSchema | None = None
    id: UUID
    primary_email: EmailSchema | None = None
    updated_at: datetime
