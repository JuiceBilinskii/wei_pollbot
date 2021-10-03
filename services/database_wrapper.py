from aiogram import types
from aiogram.dispatcher import FSMContext
import datetime

from load_all import db


async def register_user(identifier: int, first_name: str, username: str) -> None:
    """Wrapper for inserting user into database."""

    db.insert_user(identifier, first_name, username)


async def select_characters() -> dict:
    """Wrapper for selecting characters from database. Returns dictionary of dictionaries of characters."""

    character_tuples = db.select_characters()

    return {character_tuple[0]: {
        'id': character_tuple[0],
        'name': character_tuple[1],
        'height': character_tuple[2],
        'short_description': character_tuple[3],
        'url': character_tuple[4],
    } for character_tuple in character_tuples}


async def insert_poll_information(query: types.CallbackQuery, state: FSMContext) -> None:
    """Wrapper for inserting poll information (user id, data, analysis usage, concordance factor,
    answers, characters rating) in database.
    """

    data = await state.get_data()

    analysis_usage = True if query.data == 'yes' and not db.get_user_analysis_usage(query.from_user.id) else False
    poll_information = query.from_user.id, datetime.datetime.today(), analysis_usage, data.get('concordance_factor')

    db.insert_poll_answers_and_rating(poll_information, data.get('answers'), data.get('average_characters_rating'))
