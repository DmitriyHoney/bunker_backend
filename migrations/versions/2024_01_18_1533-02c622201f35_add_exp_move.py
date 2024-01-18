"""add exp move

Revision ID: 02c622201f35
Revises: f5a9353d3efe
Create Date: 2024-01-18 15:33:31.594893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02c622201f35'
down_revision: Union[str, None] = 'f5a9353d3efe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('decks_game_id_fkey', 'decks', type_='foreignkey')
    op.create_foreign_key(None, 'decks', 'games', ['game_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('games_room_id_fkey', 'games', type_='foreignkey')
    op.create_foreign_key(None, 'games', 'rooms', ['room_id'], ['id'], ondelete='CASCADE')
    op.add_column('rounds', sa.Column('status', sa.Enum('health', 'profession', 'phobia', 'hobby', 'luggage', 'quality', 'special', 'biology', 'skill', 'bunker', 'disaster', name='cardcategoryenum'), nullable=False))
    op.add_column('rounds', sa.Column('number', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rounds', 'number')
    op.drop_column('rounds', 'status')
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.create_foreign_key('games_room_id_fkey', 'games', 'rooms', ['room_id'], ['id'])
    op.drop_constraint(None, 'decks', type_='foreignkey')
    op.create_foreign_key('decks_game_id_fkey', 'decks', 'games', ['game_id'], ['id'])
    # ### end Alembic commands ###
