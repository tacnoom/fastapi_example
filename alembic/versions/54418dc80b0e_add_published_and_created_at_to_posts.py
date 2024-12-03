"""add published and created at to posts

Revision ID: 54418dc80b0e
Revises: 509c870ffd3c
Create Date: 2024-12-01 21:06:14.140504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54418dc80b0e'
down_revision: Union[str, None] = '509c870ffd3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=True, default=True))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
