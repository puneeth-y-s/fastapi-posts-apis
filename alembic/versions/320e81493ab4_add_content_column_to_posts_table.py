"""add content column to posts table

Revision ID: 320e81493ab4
Revises: b323a40a4aea
Create Date: 2024-03-05 19:27:04.868525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '320e81493ab4'
down_revision: Union[str, None] = 'b323a40a4aea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
