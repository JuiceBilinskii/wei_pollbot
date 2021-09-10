import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from load_all import dp, db
from itertools import combinations
from states import Poll
from inline_keyboards import create_character_choice
import random

@dp.message_handler(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    # db.update_user(message.chat.id, 1)
    # await state.update_data({'number_of_replies': 1})
    await message.answer(f'Этот бот предназначен для проведения опроса, результаты которого будут задействованы в дальнейшем анализе.')


@dp.message_handler(commands=['start_poll'], state=None)
async def start_poll(message: types.Message, state: FSMContext):
    characters = db.get_characters_query()
    character_combinations = list(combinations(characters, 2))
    random.shuffle(character_combinations)

    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_choice': 0})

    await message.answer('Опрос начат')
    await message.answer(f'{character_combinations[0][0][1]} - {character_combinations[0][0][2]}\n{character_combinations[0][1][1]} - {character_combinations[0][1][2]}',
    reply_markup=create_character_choice(character_combinations[0][0][1], character_combinations[0][1][1]))
    await Poll.Polling.set()
