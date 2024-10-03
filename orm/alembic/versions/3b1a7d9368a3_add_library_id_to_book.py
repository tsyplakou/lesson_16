"""Add library_id to Book.

Revision ID: 3b1a7d9368a3
Revises: 5eada7c8edfb
Create Date: 2024-10-03 20:18:45.821253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b1a7d9368a3'
down_revision: Union[str, None] = '5eada7c8edfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('library_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'book', 'library', ['library_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'book', type_='foreignkey')
    op.drop_column('book', 'library_id')
    # ### end Alembic commands ###
