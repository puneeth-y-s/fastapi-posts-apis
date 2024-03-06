"""add foreign key to posts table

Revision ID: 854b155266f4
Revises: fa2536964598
Create Date: 2024-03-06 10:40:54.071048

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '854b155266f4'
down_revision: Union[str, None] = 'fa2536964598'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
    sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
