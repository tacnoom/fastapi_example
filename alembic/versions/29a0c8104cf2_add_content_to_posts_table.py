"""add content to posts table

Revision ID: 29a0c8104cf2
Revises: 6c8b95f53e60
Create Date: 2024-12-01 20:33:14.951868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29a0c8104cf2'
down_revision: Union[str, None] = '6c8b95f53e60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
