"""create_tables

Revision ID: b15281ca2b8b
Revises: 
Create Date: 2025-03-18 23:02:48.226015

"""
from typing import Sequence, Union
import os
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b15281ca2b8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with open("database/migrations/001_create_tables.sql", "r") as sql:
        command = sql.read()

    op.execute(command)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
