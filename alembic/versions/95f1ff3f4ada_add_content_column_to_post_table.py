"""add content column to post table


Revision ID: 95f1ff3f4ada
Revises: d172ada17edd
Create Date: 2023-01-17 14:44:34.022880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95f1ff3f4ada'
down_revision = 'd172ada17edd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
