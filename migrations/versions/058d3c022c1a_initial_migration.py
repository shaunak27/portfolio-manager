"""Initial migration.

Revision ID: 058d3c022c1a
Revises: 
Create Date: 2021-04-10 21:41:25.013931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '058d3c022c1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('holdings', sa.Column('panid', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('holdings', 'panid')
    # ### end Alembic commands ###
