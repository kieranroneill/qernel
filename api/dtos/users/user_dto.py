from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from api.dtos.users import GitHubUserDTO
from api.models.users import UserModel
from api.schemas.users import UserSchema


@dataclass(slots=True)
class UserDTO:
    id: UUID
    active: bool
    created_at: datetime
    email: str
    updated_at: datetime
    display_name: str | None = None
    github: GitHubUserDTO | None = None

    @classmethod
    def from_model(cls, model: UserModel) -> "UserDTO":
        return cls(
            active=model.active,
            created_at=model.created_at,
            display_name=model.display_name,
            email=model.email,
            github=GitHubUserDTO.from_model(model.github) if model.github else None,
            id=model.id,
            updated_at=model.updated_at,
        )

    def to_model(self) -> UserModel:
        return UserModel(
            active=self.active,
            created_at=self.created_at,
            email=self.email,
            display_name=self.display_name,
            github=self.github.to_model() if self.github else None,
            id=self.id,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_schema(cls, schema: UserSchema) -> "UserDTO":
        return cls(
            active=schema.active,
            created_at=schema.created_at,
            display_name=schema.display_name,
            email=schema.email,
            github=GitHubUserDTO.from_schema(schema.github) if schema.github else None,
            id=schema.id,
            updated_at=schema.updated_at,
        )

    def to_schema(self) -> UserSchema:
        return UserSchema(
            active=self.active,
            created_at=self.created_at,
            display_name=self.display_name,
            email=self.email,
            github=self.github.to_schema() if self.github else None,
            id=self.id,
            updated_at=self.updated_at,
        )
