"""empty message

Revision ID: 4420350efa32
Revises: bc6a92132a86
Create Date: 2021-02-07 00:40:59.085067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4420350efa32'
down_revision = 'bc6a92132a86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('dt', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    # ### end Alembic commands ###
