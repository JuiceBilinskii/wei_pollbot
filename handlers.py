import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from load_all import dp, db
from itertools import combinations
from states import Poll
from inline_keyboards import create_character_choice, create_ratio_choice, create_empty, create_start_choice, create_used_in_analysis_choice
import random
import datetime

@dp.message_handler(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    await message.answer(f'Этот бот предназначен для проведения опроса, результаты которого будут задействованы в дальнейшем анализе.')
    db.insert_user_query(message.from_user.id, message.from_user.first_name, message.from_user.username)


@dp.message_handler(commands=['start_poll'], state=None)
async def start_poll(message: types.Message, state: FSMContext):
    characters = db.get_characters_query()
    character_combinations = list(combinations(characters, 2))
    random.shuffle(character_combinations)

    await Poll.Polling.set()

    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_question': 0})
    await state.update_data({'total_questions': len(character_combinations)})
    await state.update_data({'answers': []})

    await message.answer('Опрос начат')

    await message.answer(f'Данный опрос состоит из {len(character_combinations)} вопросов', reply_markup=create_start_choice())
    

@dp.callback_query_handler(text='left', state=Poll.Polling)
@dp.callback_query_handler(text='right', state=Poll.Polling)
async def process_left_character(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    if query.data == 'left':
        await state.update_data({'inverse': False})
    else:
        await state.update_data({'inverse': True})
    await message.edit_reply_markup(reply_markup=create_ratio_choice())

@dp.callback_query_handler(text='start', state=Poll.Polling)
async def send_first_question(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
        question_text = (
            f'{character_a[1]} - {character_a[2]}\n'
            f'{character_a[3]}\n\n'
            f'{character_b[1]} - {character_b[2]}\n'
            f'{character_b[3]}'
        )
        await query.message.answer(question_text, reply_markup=create_character_choice(character_a[1], character_b[1]))

@dp.callback_query_handler(text='3', state=Poll.Polling)
@dp.callback_query_handler(text='5', state=Poll.Polling)
@dp.callback_query_handler(text='7', state=Poll.Polling)
@dp.callback_query_handler(text='9', state=Poll.Polling)
async def get_answer_and_send_next_question(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())

    data = await state.get_data()

    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    ratio = 1 / int(query.data) if data.get('inverse') else int(query.data)
    await state.update_data({'answers': data.get('answers') + [(character_a[0], character_b[0], ratio)]})
    
    await state.update_data({'current_question': data.get('current_question') + 1})

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
        question_text = (
            f'{character_a[1]} - {character_a[2]}\n'
            f'{character_a[3]}\n\n'
            f'{character_b[1]} - {character_b[2]}\n'
            f'{character_b[2]}'
        )
        await query.message.answer(question_text, reply_markup=create_character_choice(character_a[1], character_b[1]))
    else:
        final_text = 'Опрос окончен. Желаете ли вы, чтобы полученные результаты были использованы в дальнейшем анализе?'
        await query.message.answer(final_text, reply_markup=create_used_in_analysis_choice())

@dp.callback_query_handler(text='yes', state=Poll.Polling)
@dp.callback_query_handler(text='no', state=Poll.Polling)
async def process_analysis_usage(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    data = await state.get_data()

    used_in_analysis = True if query.data == 'yes' else False
    poll_id = db.insert_poll_query(query.from_user.id, datetime.date.today(), used_in_analysis)
    db.inserts_answers_query(poll_id, data.get('answers'))
