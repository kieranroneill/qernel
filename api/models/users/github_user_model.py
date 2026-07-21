from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.defaults.base_model import BaseModel

if TYPE_CHECKING:
    from api.models.users.user_model import UserModel


class GitHubUserModel(BaseModel):
    __tablename__ = "github_users"
    __table_args__ = (UniqueConstraint("username", name="uq_github_users_username"),)

    # primary keys
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # data
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, onupdate=func.now(), server_default=func.now()
    )
    username: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    user: Mapped["UserModel"] = relationship(back_populates="github")
