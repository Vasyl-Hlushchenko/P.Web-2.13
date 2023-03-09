"""Init

Revision ID: a1da39857d67
Revises: 5770fefc6466
Create Date: 2023-02-19 17:22:01.941799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1da39857d67'
down_revision = '5770fefc6466'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('birthaday', sa.Date(), nullable=False))
    op.add_column('users', sa.Column('description', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'description')
    op.drop_column('users', 'birthaday')
    # ### end Alembic commands ###