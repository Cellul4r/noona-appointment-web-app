"""add notification jobs table

Revision ID: ef842e8468c6
Revises:
Create Date: 2026-03-03 10:49:36.793053

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "ef842e8468c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


notification_type_enum = sa.Enum(
    "session_reminder",
    "waitlist_available",
    "registration_summary",
    "event_updated",
    "event_cancelled",
    "registration_removed_by_host",
    name="notificationtype",
)

notification_status_enum = sa.Enum(
    "pending",
    "sent",
    "failed",
    "cancelled",
    name="notificationjobstatus",
)


def upgrade() -> None:
    bind = op.get_bind()
    notification_type_enum.create(bind, checkfirst=True)
    notification_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "notification_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM(name="notificationtype", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "status",
            postgresql.ENUM(name="notificationjobstatus", create_type=False),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=True),
        sa.Column("session_id", sa.Integer(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("dedupe_key", sa.String(length=255), nullable=True),
        sa.Column("run_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["session_id"], ["sessions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dedupe_key"),
    )

    op.create_index(
        op.f("ix_notification_jobs_id"), "notification_jobs", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_notification_jobs_type"), "notification_jobs", ["type"], unique=False
    )
    op.create_index(
        op.f("ix_notification_jobs_status"),
        "notification_jobs",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_jobs_user_id"),
        "notification_jobs",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_jobs_event_id"),
        "notification_jobs",
        ["event_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_jobs_session_id"),
        "notification_jobs",
        ["session_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_notification_jobs_run_at"),
        "notification_jobs",
        ["run_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_notification_jobs_run_at"), table_name="notification_jobs")
    op.drop_index(
        op.f("ix_notification_jobs_session_id"), table_name="notification_jobs"
    )
    op.drop_index(op.f("ix_notification_jobs_event_id"), table_name="notification_jobs")
    op.drop_index(op.f("ix_notification_jobs_user_id"), table_name="notification_jobs")
    op.drop_index(op.f("ix_notification_jobs_status"), table_name="notification_jobs")
    op.drop_index(op.f("ix_notification_jobs_type"), table_name="notification_jobs")
    op.drop_index(op.f("ix_notification_jobs_id"), table_name="notification_jobs")
    op.drop_table("notification_jobs")

    bind = op.get_bind()
    notification_status_enum.drop(bind, checkfirst=True)
    notification_type_enum.drop(bind, checkfirst=True)
