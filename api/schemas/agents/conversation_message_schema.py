from datetime import datetime
from uuid import UUID

from pydantic import Field

from api.enums.agents import MessageRoleEnum, MessageStatusEnum
from api.schemas.defaults import BaseSchema


class ConversationMessageSchema(BaseSchema):
    id: UUID
    build_id: UUID
    content: str
    created_at: datetime
    extra_data: dict = Field(default_factory=dict)
    input_tokens: int | None = None
    internal: bool = False
    model: str | None = None
    name: str | None = None
    output_tokens: int | None = None
    parent_message_id: UUID | None = None
    role: MessageRoleEnum
    sequence_number: int
    status: MessageStatusEnum = MessageStatusEnum.PENDING
    total_tokens: int | None = None
    updated_at: datetime
