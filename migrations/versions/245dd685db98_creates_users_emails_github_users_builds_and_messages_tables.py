"""creates users, emails, github_users, builds and messages tables

Revision ID: 245dd685db98
Revises:
Create Date: 2026-07-21 10:03:53.792085

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "245dd685db98"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # creates "users" table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("primary_email_id", sa.UUID(), nullable=True),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("primary_email_id"),
    )
    op.create_index("ix_users_active", "users", ["active"], unique=False)

    # creates "emails" table
    op.create_table(
        "emails",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("verified", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_emails_email"),
    )
    op.create_index("ix_emails_verified", "emails", ["verified"], unique=False)

    # creates "github_users" table
    op.create_table(
        "github_users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("username", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
        sa.UniqueConstraint("username", name="uq_github_users_username"),
    )

    # creates "builds" table
    op.create_table(
        "builds",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "extra_data", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column("project_name", sa.String(length=200), nullable=True),
        sa.Column(
            "resolved_variables",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "stage",
            sa.Enum("initiated", "plan", "validate", "ready", name="build_stage_enum"),
            server_default=sa.text("'initiated'"),
            nullable=False,
        ),
        sa.Column(
            "selected_feature_packs", postgresql.ARRAY(sa.Text()), server_default=sa.text("'{}'"), nullable=False
        ),
        sa.Column("template_id", sa.String(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_builds_active", "builds", ["active"], unique=False)
    op.create_index("ix_builds_stage", "builds", ["stage"], unique=False)
    op.create_index("ix_builds_template_id", "builds", ["template_id"], unique=False)

    # creates "conversation_messages" table
    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("build_id", sa.UUID(), nullable=False),
        sa.Column("parent_message_id", sa.UUID(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "extra_data", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'{}'::jsonb"), nullable=False
        ),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("internal", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("role", sa.Enum("assistant", "user", "system", name="message_role_enum"), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("completed", "failed", "pending", name="message_status_enum"),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("total_tokens", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["build_id"], ["builds.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["parent_message_id"], ["conversation_messages.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("build_id", "sequence_number", name="uq_message_build_sequence"),
    )
    op.create_index("ix_message_build_created", "conversation_messages", ["build_id", "created_at"], unique=False)
    op.create_index("ix_message_build_sequence", "conversation_messages", ["build_id", "sequence_number"], unique=False)
    op.create_index("ix_message_build_status", "conversation_messages", ["build_id", "status"], unique=False)

    # adds foreign key relationships to avoid circular references
    op.create_foreign_key(
        "fk_users_primary_email_id_emails",
        "users",
        "emails",
        ["primary_email_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # delete constraints
    op.drop_constraint("fk_users_primary_email_id_emails", "users", type_="foreignkey")

    # drop "conversation_messages" table
    op.drop_index("ix_message_build_status", table_name="conversation_messages")
    op.drop_index("ix_message_build_sequence", table_name="conversation_messages")
    op.drop_index("ix_message_build_created", table_name="conversation_messages")
    op.drop_table("conversation_messages")

    # drop "builds" table
    op.drop_index("ix_builds_template_id", table_name="builds")
    op.drop_index("ix_builds_stage", table_name="builds")
    op.drop_index("ix_builds_active", table_name="builds")
    op.drop_table("builds")

    # drop "github_users" table
    op.drop_table("github_users")

    # drop "emails" table
    op.drop_index("ix_emails_verified", table_name="emails")
    op.drop_table("emails")

    # drop "users" table
    op.drop_index("ix_users_active", table_name="users")
    op.drop_table("users")
