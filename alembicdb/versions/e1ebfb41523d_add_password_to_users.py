"""Add password to users

Revision ID: e1ebfb41523d
Revises: 29b594989ff3
Create Date: 2021-03-23 12:27:09.492275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1ebfb41523d'
down_revision = '29b594989ff3'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('users', sa.Column('password_hash', sa.String))


def downgrade():
  op.drop_column('users', 'password_hash')
