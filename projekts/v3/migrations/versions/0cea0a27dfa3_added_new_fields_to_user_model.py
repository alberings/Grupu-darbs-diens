"""Added new fields to User model

Revision ID: 0cea0a27dfa3
Revises: b13566accc3b
Create Date: 2023-12-14 12:34:09.822061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cea0a27dfa3'
down_revision = 'b13566accc3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('weight', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('activity_level', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('dietary_restrictions', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('allergies', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('allergies')
        batch_op.drop_column('dietary_restrictions')
        batch_op.drop_column('activity_level')
        batch_op.drop_column('gender')
        batch_op.drop_column('age')
        batch_op.drop_column('weight')
        batch_op.drop_column('height')

    # ### end Alembic commands ###