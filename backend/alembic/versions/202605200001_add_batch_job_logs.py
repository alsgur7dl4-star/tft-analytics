"""add batch_job_logs table

Revision ID: 202605200001
Revises: 202605180001
Create Date: 2026-05-20
"""

import sqlalchemy as sa
from alembic import op

revision = "202605200001"
down_revision = "202605180001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "batch_job_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "job_run_id",
            sa.Integer(),
            sa.ForeignKey("batch_job_runs.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("log_level", sa.String(20), nullable=False, server_default="INFO"),
        sa.Column("step", sa.String(120), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("meta_json", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("batch_job_logs")
