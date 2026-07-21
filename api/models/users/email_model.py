from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Text,
    UniqueConstraint,
    false,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.defaults.base_model import BaseModel

if TYPE_CHECKING:
    from api.models.users.user_model import UserModel


class EmailModel(BaseModel):
    __tablename__ = "emails"
    __table_args__ = (
        UniqueConstraint("email", name="uq_emails_email"),
        Index("ix_emails_verified", "verified"),
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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    email: Mapped[str] = mapped_column(Text, nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default=false())

    # relationships
    user: Mapped["UserModel"] = relationship(back_populates="emails", foreign_keys=[user_id])
