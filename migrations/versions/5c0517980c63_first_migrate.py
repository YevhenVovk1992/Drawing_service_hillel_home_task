"""First migrate

Revision ID: 5c0517980c63
Revises: 
Create Date: 2022-09-12 11:56:35.392484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c0517980c63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task_queue',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_queue')
    # ### end Alembic commands ###
