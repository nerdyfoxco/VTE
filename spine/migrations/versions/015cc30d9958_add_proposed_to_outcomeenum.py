"""Add PROPOSED to OutcomeEnum

Revision ID: 015cc30d9958
Revises: 8e58b21da540
Create Date: 2026-02-04 11:43:27.949670

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '015cc30d9958'
down_revision: Union[str, None] = '8e58b21da540'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Manual Enum Update for Postgres
    # Cannot run ALTER TYPE ... ADD VALUE inside a transaction block in older Postgres, 
    # but in newer ones it is fine.
    # Alembic runs in transaction by default.
    # To be safe against "ERROR: ALTER TYPE ... ADD VALUE cannot run inside a transaction block" (if old PG),
    # we would need to commit. But let's assume Pg 12+.
    
    op.execute("ALTER TYPE outcome_enum ADD VALUE IF NOT EXISTS 'PROPOSED' BEFORE 'APPROVED'")


def downgrade() -> None:
    # Postgres ENUM types do not support removing values easily.
    # We would need to rename type, create new type without value, migrate columns, drop old type.
    # For now, we skip downgrade logic or just warn.
    pass
