"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, exists, ScalarResult
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import CurrentUser
from core import exceptions
from core.models import Game, GameStatusEnum, User, Room
from .schemas import GameCreate, GameUpdate, GameUpdatePartial


async def get_games(session: AsyncSession, user_id: int | None) -> list[Game]:
    query = select(Game).order_by(Game.id)
    if user_id:
        query = query.join(Room).join(User).filter(User.id == user_id)

    return (await session.scalars(query)).all()


async def get_game(session: AsyncSession, game_id: int) -> Game | None:
    return await session.get(Game, game_id)


async def create_game(session: AsyncSession, game_in: GameCreate) -> Game:

    query = exists(Game).where(Game.room_id == game_in.room_id, Game.status == GameStatusEnum.playing).select()
    games_exists = await session.scalar(query)

    if games_exists:
        raise exceptions.APIException(detail="Активные игры в комнате уже существуют")

    game = Game(status=GameStatusEnum.playing, **game_in.model_dump())
    session.add(game)

    # await session.flush()
    # await session.refresh(game)
    #
    # users = game.room.users
    # random_decks = await get_random_cards_deck(session=session, limit=len(users))
    #
    # for i, user in enumerate(game.room.users):
    #     deck = Deck()
    #     deck.game = game
    #     deck.user = user
    #     deck.cards = random_decks[i]
    #     session.add(deck)
    #
    # create_rounds(game)
    #
    # for i in range(9):
    #     round = Round(name=f"round_{i + 1}")

    await session.commit()
    await session.refresh(game)
    return game


async def update_game(
    session: AsyncSession,
    game: Game,
    game_update: GameUpdate | GameUpdatePartial,
    partial: bool = False,
) -> Game:
    for name, value in game_update.model_dump(exclude_unset=partial).items():
        setattr(game, name, value)
    await session.commit()
    return game


async def delete_game(
    session: AsyncSession,
    game: Game,
) -> None:
    await session.delete(game)
    await session.commit()


