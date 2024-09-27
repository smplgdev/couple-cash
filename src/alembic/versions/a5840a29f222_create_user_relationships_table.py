"""Create user_relationships table

Revision ID: a5840a29f222
Revises: 6593d098ec67
Create Date: 2024-09-27 23:20:57.559257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5840a29f222'
down_revision: Union[str, None] = '6593d098ec67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_relationships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('initiating_user_tg_id', sa.BigInteger(), nullable=False),
    sa.Column('partner_user_tg_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['initiating_user_tg_id'], ['users.tg_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['partner_user_tg_id'], ['users.tg_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('initiating_user_tg_id', 'partner_user_tg_id', name='unique_relationship')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_relationships')
    # ### end Alembic commands ###