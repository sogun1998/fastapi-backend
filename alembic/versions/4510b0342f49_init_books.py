"""init books

Revision ID: 4510b0342f49
Revises: 2409e1c6cb32
Create Date: 2025-07-21 05:45:46.999173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4510b0342f49'
down_revision: Union[str, Sequence[str], None] = '2409e1c6cb32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('books',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('author_id', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_table('books')
