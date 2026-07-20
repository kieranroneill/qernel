from dataclasses import dataclass
from datetime import datetime

from api.models.users import GitHubUserModel
from api.schemas.users import GitHubUserSchema


@dataclass(slots=True)
class GitHubUserDTO:
    created_at: datetime
    id: int
    updated_at: datetime
    username: str

    @classmethod
    def from_model(cls, model: GitHubUserModel) -> "GitHubUserDTO":
        return cls(
            created_at=model.created_at,
            id=model.id,
            updated_at=model.updated_at,
            username=model.username,
        )

    def to_model(self) -> GitHubUserModel:
        return GitHubUserModel(
            created_at=self.created_at,
            id=self.id,
            updated_at=self.updated_at,
            username=self.username,
        )

    @classmethod
    def from_schema(cls, schema: GitHubUserSchema) -> "GitHubUserDTO":
        return cls(
            created_at=schema.created_at,
            id=schema.id,
            updated_at=schema.updated_at,
            username=schema.username,
        )

    def to_schema(self) -> GitHubUserSchema:
        return GitHubUserSchema(
            created_at=self.created_at,
            id=self.id,
            updated_at=self.updated_at,
            username=self.username,
        )
