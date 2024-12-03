"""add users table

Revision ID: 0f4632a1584a
Revises: 29a0c8104cf2
Create Date: 2024-12-01 20:47:14.112442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f4632a1584a'
down_revision: Union[str, None] = '29a0c8104cf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False,unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'),nullable=True),
                    # sa.PrimaryKeyConstraint('id'),
                    # sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
