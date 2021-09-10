import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from load_all import dp, db
from itertools import combinations
from states import Poll
from inline_keyboards import create_character_choice, create_ratio_choice, create_empty
import random

@dp.message_handler(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    await message.answer(f'Этот бот предназначен для проведения опроса, результаты которого будут задействованы в дальнейшем анализе.')


@dp.message_handler(commands=['start_poll'], state=None)
async def start_poll(message: types.Message, state: FSMContext):
    characters = db.get_characters_query()
    character_combinations = list(combinations(characters, 2))
    random.shuffle(character_combinations)

    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_question': 0})
    await state.update_data({'total_questions': len(character_combinations)})

    await message.answer('Опрос начат')

    text, keyboard = await create_question(state)
    await message.answer(text, reply_markup=keyboard)

    await Poll.Polling.set()
    

@dp.callback_query_handler(text='left', state=Poll.Polling)
async def process_left_character(query: types.CallbackQuery):
    message = query.message
    await message.edit_reply_markup(reply_markup=create_ratio_choice())

@dp.callback_query_handler(text='right', state=Poll.Polling)
async def process_right_character(query: types.CallbackQuery):
    message = query.message
    await message.edit_reply_markup(reply_markup=create_empty())

@dp.callback_query_handler(text='3', state=Poll.Polling)
@dp.callback_query_handler(text='5', state=Poll.Polling)
@dp.callback_query_handler(text='7', state=Poll.Polling)
@dp.callback_query_handler(text='9', state=Poll.Polling)
async def send_question(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())

    data = await state.get_data()

    question_number = data.get('current_question')

    message = query.message
    if question_number < data.get('total_questions'):
        text, keyboard = await create_question(state)
        await message.answer(text, reply_markup=keyboard)
    else:
        await message.answer('Опрос окончен')

async def create_question(state: FSMContext):
    data = await state.get_data()

    question_number = data.get('current_question')
    character_a, character_b = data.get('characters_combinations')[question_number]

    text = f"{character_a[1]} - {character_a[2]}\n{character_a[3]}\n\n{character_b[1]} - {character_b[2]}\n{character_b[3]}"
    keyboard = create_character_choice(character_a[1], character_b[1])

    await state.update_data({'current_question': question_number + 1})
    return text, keyboard
