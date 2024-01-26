from sqlalchemy.ext.asyncio import AsyncSession

from api.decks.crud import get_deck_by_game_user
from api.moves.crud import add_card_to_move
from core import exceptions
from core.models import Move, Card, Deck, User


async def remove_card_in_deck(session: AsyncSession, deck: Deck, card: Card):
    deck.cards.remove(card)
    session.commit()


async def make_move_card(session: AsyncSession, move: Move, card: Card, user: User):

    if move.card:
        raise exceptions.APIException(detail="Ход уже сделан")

    deck = await get_deck_by_game_user(
        session=session,
        user_id=move.user.id,
        game_id=move.round and move.round.game.id
    )

    if card not in deck.cards:
        raise exceptions.APIException(detail="Карты нет в колоде игорока")

    move = await add_card_to_move(session=session, move=move, card=card)
    await remove_card_in_deck(session=session, deck=deck, card=card)
    return move
