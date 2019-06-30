"""Add new column

Revision ID: 01dae0bc2185
Revises: 3a1b4630f3e9
Create Date: 2019-06-30 15:43:07.297933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01dae0bc2185'
down_revision = '3a1b4630f3e9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('test', sa.String(length=140),nullable=True))



def downgrade():
    op.drop_column('users', 'test')
