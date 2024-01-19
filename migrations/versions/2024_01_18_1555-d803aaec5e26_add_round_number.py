"""add round number

Revision ID: d803aaec5e26
Revises: 02c622201f35
Create Date: 2024-01-18 15:55:01.631260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd803aaec5e26'
down_revision: Union[str, None] = '02c622201f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rounds', sa.Column('state', sa.Enum('waiting', 'playing', 'played', name='roundstateenum'), nullable=False))
    op.drop_column('rounds', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rounds', sa.Column('status', postgresql.ENUM('health', 'profession', 'phobia', 'hobby', 'luggage', 'quality', 'special', 'biology', 'skill', 'bunker', 'disaster', name='cardcategoryenum'), autoincrement=False, nullable=False))
    op.drop_column('rounds', 'state')
    # ### end Alembic commands ###