import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    false,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.enums.agents import MessageRoleEnum, MessageStatusEnum
from api.models.defaults.base_model import BaseModel

if TYPE_CHECKING:
    from api.models.builds.build_model import BuildModel


class ConversationMessageModel(BaseModel):
    __tablename__ = "conversation_messages"
    __table_args__ = (
        UniqueConstraint("build_id", "sequence_number", name="uq_message_build_sequence"),
        Index("ix_message_build_created", "build_id", "created_at"),
        Index("ix_message_build_sequence", "build_id", "sequence_number"),
        Index("ix_message_build_status", "build_id", "status"),
    )

    # primary keys
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # foreign keys
    build_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("builds.id", ondelete="RESTRICT"),
        nullable=False,
    )
    parent_message_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversation_messages.id", ondelete="SET NULL"),
        nullable=True,
    )

    # data
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False, server_default=text("'{}'::jsonb"))
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    internal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default=false())
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    role: Mapped[MessageRoleEnum] = mapped_column(
        Enum(MessageRoleEnum, name="message_role_enum", values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[MessageStatusEnum] = mapped_column(
        Enum(
            MessageStatusEnum, name="message_status_enum", values_callable=lambda enum_cls: [e.value for e in enum_cls]
        ),
        default=MessageStatusEnum.PENDING,
        nullable=False,
        server_default=text("'pending'"),
    )
    total_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, onupdate=func.now(), server_default=func.now()
    )

    # relationships
    build: Mapped["BuildModel"] = relationship(back_populates="messages")
