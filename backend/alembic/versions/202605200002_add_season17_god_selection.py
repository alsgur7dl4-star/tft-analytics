"""add season17 god selection: tft_static_gods table, god columns

Revision ID: 202605200002
Revises: 202605200001
Create Date: 2026-05-20
"""

import sqlalchemy as sa
from alembic import op

revision = "202605200002"
down_revision = "202605200001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tft_static_gods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("god_key", sa.String(120), nullable=False, unique=True, index=True),
        sa.Column("god_name", sa.String(160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("passive_desc", sa.Text(), nullable=True),
        sa.Column("set_name", sa.String(40), nullable=True),
        sa.Column("icon_url", sa.String(255), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "tft_match_participants",
        sa.Column("selected_god_key", sa.String(120), nullable=True),
    )
    op.create_index("ix_tft_match_participants_selected_god_key", "tft_match_participants", ["selected_god_key"])

    op.add_column(
        "tft_comps",
        sa.Column("preferred_gods_json", sa.JSON(), nullable=True),
    )

    op.add_column(
        "tft_recommendation_logs",
        sa.Column("input_gods_json", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("tft_recommendation_logs", "input_gods_json")
    op.drop_column("tft_comps", "preferred_gods_json")
    op.drop_index("ix_tft_match_participants_selected_god_key", "tft_match_participants")
    op.drop_column("tft_match_participants", "selected_god_key")
    op.drop_table("tft_static_gods")
