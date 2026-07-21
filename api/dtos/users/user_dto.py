from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from api.dtos.users import EmailDTO, GitHubUserDTO
from api.models.users import UserModel
from api.schemas.users import UserSchema


@dataclass(slots=True)
class UserDTO:
    id: UUID
    active: bool
    created_at: datetime
    updated_at: datetime
    display_name: str | None = None
    emails: list[EmailDTO] = field(default_factory=list)
    github: GitHubUserDTO | None = None
    primary_email: EmailDTO | None = None

    @classmethod
    def from_model(cls, model: UserModel) -> "UserDTO":
        return cls(
            active=model.active,
            created_at=model.created_at,
            display_name=model.display_name,
            emails=[EmailDTO.from_model(email) for email in model.emails],
            github=GitHubUserDTO.from_model(model.github) if model.github else None,
            id=model.id,
            primary_email=EmailDTO.from_model(model.primary_email) if model.primary_email else None,
            updated_at=model.updated_at,
        )

    def to_model(self) -> UserModel:
        return UserModel(
            active=self.active,
            created_at=self.created_at,
            emails=[email.to_model() for email in self.emails],
            display_name=self.display_name,
            github=self.github.to_model() if self.github else None,
            id=self.id,
            primary_email=self.primary_email.to_model() if self.primary_email else None,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_schema(cls, schema: UserSchema) -> "UserDTO":
        return cls(
            active=schema.active,
            created_at=schema.created_at,
            display_name=schema.display_name,
            emails=[EmailDTO.from_schema(email) for email in schema.emails],
            github=GitHubUserDTO.from_schema(schema.github) if schema.github else None,
            id=schema.id,
            primary_email=EmailDTO.from_schema(schema.primary_email) if schema.primary_email else None,
            updated_at=schema.updated_at,
        )

    def to_schema(self) -> UserSchema:
        return UserSchema(
            active=self.active,
            created_at=self.created_at,
            display_name=self.display_name,
            emails=[email.to_schema() for email in self.emails],
            github=self.github.to_schema() if self.github else None,
            id=self.id,
            primary_email=self.primary_email.to_schema() if self.primary_email else None,
            updated_at=self.updated_at,
        )
