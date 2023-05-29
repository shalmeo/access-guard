"""[sessions]: add table

Revision ID: ffafc9c24b26
Revises: 22c6e30770b8
Create Date: 2023-05-24 14:53:23.556013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffafc9c24b26'
down_revision = '22c6e30770b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('session_id', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('fk_sessions_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('session_id', name=op.f('pk_sessions'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    # ### end Alembic commands ###
