from sqlalchemy.ext.asyncio import AsyncSession

from api.decks.crud import get_deck_by_game_user
from core import exceptions
from core.models import Move, Card


async def remove_card_in_deck(session: AsyncSession, move: Move, card: Card):
    if move.card:
        raise exceptions.APIException(detail="Ход уже сделан")

    deck = await get_deck_by_game_user(
        session=session,
        user_id=move.user.id,
        game_id=move.round and move.round.game.id
    )

    if card not in deck.cards:
        raise exceptions.APIException(detail="Карты нет в колоде игорока")

    deck.cards.remove(card)

    session.commit()
