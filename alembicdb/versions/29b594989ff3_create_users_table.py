"""create users table

Revision ID: 29b594989ff3
Revises: 
Create Date: 2021-03-23 11:59:27.351613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29b594989ff3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'users',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('email', sa.String(100), nullable=False, unique=True)
  )


def downgrade():
  op.drop_table('users')
