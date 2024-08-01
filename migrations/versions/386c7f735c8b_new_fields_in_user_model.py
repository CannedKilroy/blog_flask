"""new fields in user model

Revision ID: 386c7f735c8b
Revises: 9b210ea505be
Create Date: 2024-07-27 21:07:43.291716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '386c7f735c8b'
down_revision = '9b210ea505be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
