"""Add new column

Revision ID: 2572ee835554
Revises: 49042ad93512
Create Date: 2019-06-30 08:46:08.225023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2572ee835554'
down_revision = '49042ad93512'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('test', sa.String(length=140),nullable=True))


def downgrade():
    op.drop_column('users', 'test')
