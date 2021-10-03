import random
from itertools import combinations

from aiogram import types
from aiogram.dispatcher import FSMContext

from services.inline_keyboards import (create_character_choice_keyboard, create_ratio_choice, create_empty,
                                       create_analysis_usage_choice, create_start_poll_keyboard)

from services import (create_post_poll_question_text,
                      receive_answer, create_next_question, complete_poll)

from load_all import dp
from services.states import Poll
from services.database_wrapper import select_characters, insert_poll_information
from services.messages_text import create_characters_list_text, create_stop_poll_text


@dp.message_handler(commands=['start_poll'], state=None)
async def initialize_poll(message: types.Message, state: FSMContext):
    characters_dict = await select_characters()

    if not characters_dict:
        return

    character_combinations = list(combinations(characters_dict.values(), 2))
    random.shuffle(character_combinations)

    await state.update_data({'characters': characters_dict})
    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_question': 0})
    await state.update_data({'total_questions': len(character_combinations)})
    await state.update_data({'answers': []})

    message_text = (f'Количество пар: {len(character_combinations)}\n\n'
                    f'Список пероснажей:\n{create_characters_list_text(characters_dict.values())}'
                    f'\n\n'
                    f'Для каждой пары персонажей вам нужно выбрать относительную оценку силы от 1 до 9 '
                    f'в пользу одного из них. 1 означает, что персонажи равны между собой, а 9, соотвественно, '
                    f'означает, что один из персонажей значительно довлеет над другим')

    await message.answer(message_text, reply_markup=create_start_poll_keyboard(), disable_web_page_preview=True)


@dp.callback_query_handler(text='start', state=None)
async def handle_first_question(query: types.CallbackQuery, state: FSMContext):
    await Poll.Polling.set()

    data = await state.get_data()

    diagonal_answers = []
    for character_id in data.get('characters'):
        diagonal_answers.append((character_id, character_id, 1))

    await state.update_data({'answers': data.get('answers') + [*diagonal_answers]})

    question_text, character_a, character_b = await create_next_question(data)

    await query.message.edit_reply_markup(reply_markup=create_empty())
    await query.message.answer(question_text,
                               reply_markup=create_character_choice_keyboard(character_a['name'], character_b['name']),
                               disable_web_page_preview=True)


@dp.callback_query_handler(text='left', state=Poll.Polling)
@dp.callback_query_handler(text='right', state=Poll.Polling)
async def handle_character_choice(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    await state.update_data({'inverse': False}) if query.data == 'left' else await state.update_data({'inverse': True})
    await message.edit_reply_markup(reply_markup=create_ratio_choice())


@dp.callback_query_handler(lambda c: c.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9'), state=Poll.Polling)
async def handle_characters_ratio_choice(query: types.CallbackQuery, state: FSMContext):
    await receive_answer(query.data, state)

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        question_text, character_a, character_b = await create_next_question(data)
        character_choice_keyboard = create_character_choice_keyboard(character_a['name'], character_b['name'])
        await query.message.edit_text(question_text,
                                      reply_markup=character_choice_keyboard,
                                      disable_web_page_preview=True)
    else:
        question_text = create_post_poll_question_text(data)
        await query.message.edit_text(question_text, disable_web_page_preview=True, reply_markup=create_empty())

        complete_message_text = await complete_poll(data, state)
        await query.message.answer(complete_message_text, reply_markup=create_analysis_usage_choice())


@dp.callback_query_handler(text='yes', state=Poll.Polling)
@dp.callback_query_handler(text='no', state=Poll.Polling)
async def handle_analysis_usage_choice(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())

    await insert_poll_information(query, state)

    await query.message.answer('Спасибо за участие в опросе.')
    await state.finish()


@dp.callback_query_handler(text='stop', state=Poll.Polling)
async def handle_stop_choice(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    await query.message.answer(create_stop_poll_text())
    await state.finish()


@dp.callback_query_handler(text='cancel', state=Poll.Polling)
async def handle_cancel_choice(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    await query.message.edit_reply_markup(reply_markup=create_character_choice_keyboard(character_a['name'],
                                                                                        character_b['name']))
