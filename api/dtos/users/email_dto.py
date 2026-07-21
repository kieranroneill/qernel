from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from api.models.users import EmailModel
from api.schemas.users import EmailSchema


@dataclass(slots=True)
class EmailDTO:
    created_at: datetime
    email: str
    id: UUID
    verified: bool

    @classmethod
    def from_model(cls, model: EmailModel) -> "EmailDTO":
        return cls(
            created_at=model.created_at,
            email=model.email,
            id=model.id,
            verified=model.verified,
        )

    def to_model(self) -> EmailModel:
        return EmailModel(
            created_at=self.created_at,
            email=self.email,
            id=self.id,
            verified=self.verified,
        )

    @classmethod
    def from_schema(cls, schema: EmailSchema) -> "EmailDTO":
        return cls(
            created_at=schema.created_at,
            email=schema.email,
            id=schema.id,
            verified=schema.verified,
        )

    def to_schema(self) -> EmailSchema:
        return EmailSchema(
            created_at=self.created_at,
            email=self.email,
            id=self.id,
            verified=self.verified,
        )
