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
    func,
    true,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models.defaults.base_model import BaseModel

if TYPE_CHECKING:
    from api.models.builds.build_model import BuildModel
    from api.models.users.email_model import EmailModel
    from api.models.users.github_user_model import GitHubUserModel


class UserModel(BaseModel):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_active", "active"),)

    # primary keys
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # foreign keys
    primary_email_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("emails.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    # data
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, server_default=true())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    display_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, onupdate=func.now(), server_default=func.now()
    )

    # relationships
    builds: Mapped[list["BuildModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="BuildModel.user_id",
    )
    emails: Mapped[list["EmailModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="EmailModel.user_id",
    )
    github: Mapped["GitHubUserModel | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    primary_email: Mapped["EmailModel | None"] = relationship(
        foreign_keys=[primary_email_id],
        post_update=True,
        uselist=False,
    )
