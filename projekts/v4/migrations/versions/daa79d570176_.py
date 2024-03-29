"""empty message

Revision ID: daa79d570176
Revises: 0cea0a27dfa3
Create Date: 2023-12-15 13:58:27.832076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa79d570176'
down_revision = '0cea0a27dfa3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('menu_plan', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('menu_plan')

    # ### end Alembic commands ###
