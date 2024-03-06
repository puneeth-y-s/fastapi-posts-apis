"""add last few columns to posts table

Revision ID: 5a09969b8349
Revises: 854b155266f4
Create Date: 2024-03-06 10:52:18.808596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a09969b8349'
down_revision: Union[str, None] = '854b155266f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
    sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE")
    )
    op.add_column('posts',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
    )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
