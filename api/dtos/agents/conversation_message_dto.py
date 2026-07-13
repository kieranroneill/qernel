from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from api.enums.agents import MessageRoleEnum, MessageStatusEnum
from api.models.agents import ConversationMessageModel
from api.schemas.agents import ConversationMessageSchema


@dataclass(slots=True)
class ConversationMessageDTO:
    id: UUID
    build_id: UUID
    content: str
    created_at: datetime
    role: MessageRoleEnum
    sequence_number: int
    updated_at: datetime
    extra_data: dict = field(default_factory=dict)
    status: MessageStatusEnum = MessageStatusEnum.PENDING
    parent_message_id: UUID | None = None
    input_tokens: int | None = None
    internal: bool = False
    model: str | None = None
    name: str | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

    @classmethod
    def from_model(cls, model: ConversationMessageModel) -> "ConversationMessageDTO":
        return cls(
            id=model.id,
            build_id=model.build_id,
            content=model.content,
            created_at=model.created_at,
            extra_data=dict(model.extra_data),
            role=model.role,
            sequence_number=model.sequence_number,
            status=model.status,
            updated_at=model.updated_at,
            parent_message_id=model.parent_message_id,
            input_tokens=model.input_tokens,
            internal=model.internal,
            model=model.model,
            name=model.name,
            output_tokens=model.output_tokens,
            total_tokens=model.total_tokens,
        )

    def to_model(self) -> ConversationMessageModel:
        return ConversationMessageModel(
            id=self.id,
            build_id=self.build_id,
            content=self.content,
            created_at=self.created_at,
            extra_data=dict(self.extra_data),
            role=self.role,
            sequence_number=self.sequence_number,
            status=self.status,
            updated_at=self.updated_at,
            parent_message_id=self.parent_message_id,
            input_tokens=self.input_tokens,
            internal=self.internal,
            model=self.model,
            name=self.name,
            output_tokens=self.output_tokens,
            total_tokens=self.total_tokens,
        )

    @classmethod
    def from_schema(cls, schema: ConversationMessageSchema) -> "ConversationMessageDTO":
        return cls(
            id=schema.id,
            build_id=schema.build_id,
            content=schema.content,
            created_at=schema.created_at,
            extra_data=dict(schema.extra_data),
            role=schema.role,
            sequence_number=schema.sequence_number,
            status=schema.status,
            updated_at=schema.updated_at,
            parent_message_id=schema.parent_message_id,
            input_tokens=schema.input_tokens,
            internal=schema.internal,
            model=schema.model,
            name=schema.name,
            output_tokens=schema.output_tokens,
            total_tokens=schema.total_tokens,
        )

    def to_schema(self) -> ConversationMessageSchema:
        return ConversationMessageSchema(
            id=self.id,
            build_id=self.build_id,
            content=self.content,
            created_at=self.created_at,
            extra_data=dict(self.extra_data),
            role=self.role,
            sequence_number=self.sequence_number,
            status=self.status,
            updated_at=self.updated_at,
            parent_message_id=self.parent_message_id,
            input_tokens=self.input_tokens,
            internal=self.internal,
            model=self.model,
            name=self.name,
            output_tokens=self.output_tokens,
            total_tokens=self.total_tokens,
        )
