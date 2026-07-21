from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    func,
    text,
    true,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.enums.builds import BuildStageEnum
from api.models.defaults.base_model import BaseModel

if TYPE_CHECKING:
    from api.models.agents.conversation_message_model import ConversationMessageModel
    from api.models.users.user_model import UserModel


class BuildModel(BaseModel):
    __tablename__ = "builds"
    __table_args__ = (
        Index("ix_builds_template_id", "template_id"),
        Index("ix_builds_stage", "stage"),
        Index("ix_builds_active", "active"),
    )

    # primary keys
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # data
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, server_default=true())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False, server_default=text("'{}'::jsonb"))
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    resolved_variables: Mapped[dict] = mapped_column(
        JSONB, default=dict, nullable=False, server_default=text("'{}'::jsonb")
    )
    stage: Mapped[BuildStageEnum] = mapped_column(
        Enum(BuildStageEnum, name="build_stage_enum", values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        default=BuildStageEnum.INITIATED,
        nullable=False,
        server_default=text("'initiated'"),
    )
    selected_feature_packs: Mapped[list[str]] = mapped_column(
        ARRAY(Text), default=list, nullable=False, server_default=text("'{}'")
    )
    template_id: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, onupdate=func.now(), server_default=func.now()
    )

    # relationships
    messages: Mapped[list["ConversationMessageModel"]] = relationship(
        back_populates="build",
        cascade="all, delete-orphan",
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="builds",
        foreign_keys=[user_id],
    )
