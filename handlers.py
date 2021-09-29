import datetime
import random
from itertools import combinations

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from inline_keyboards import (create_character_choice, create_ratio_choice, create_empty,
                              create_analysis_usage_choice)
from load_all import dp, db
from states import Poll


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    db.insert_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    start_text = (f'Теперь можете приступить к прохождению опроса. Вам предстоит выполнить ряд '
                  f'попарных сравнений между персонажами на предмет оценки их относительной силы. '
                  f'Естественно подразумевается, что сравнивается не физическая сила в прямом '
                  f'смысле, а берется во внимание ряд менее конкретных качеств и просто степень влияния '
                  f'персонажей на сюжет.')
    await message.answer(start_text)


@dp.message_handler(commands=['start_poll'], state=None)
async def start_poll(message: types.Message, state: FSMContext):
    characters = db.select_characters()
    character_combinations = list(combinations(characters, 2))
    random.shuffle(character_combinations)

    await Poll.Polling.set()

    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_question': 0})
    await state.update_data({'total_questions': len(character_combinations)})
    await state.update_data({'answers': []})

    await message.answer(f'Количество пар: {len(character_combinations)}')

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        diagonal_answers = []
        for character in characters:
            diagonal_answers.append((character[0], character[0], 1))

        await state.update_data({'answers': data.get('answers') + [*diagonal_answers]})

        question_text, character_a, character_b = create_question_text(data)
        await message.answer(question_text, reply_markup=create_character_choice(character_a[1], character_b[1]))


@dp.callback_query_handler(text='left', state=Poll.Polling)
@dp.callback_query_handler(text='right', state=Poll.Polling)
async def process_character_choice(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    await state.update_data({'inverse': False}) if query.data == 'left' else await state.update_data({'inverse': True})
    await message.edit_reply_markup(reply_markup=create_ratio_choice())


def create_question_text(data):
    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    return (
        f'{data.get("current_question") + 1}/{data.get("total_questions")}\n\n'
        f'{character_a[1]} - {character_a[2]}\n'
        f'{character_a[3]}\n\n'
        f'{character_b[1]} - {character_b[2]}\n'
        f'{character_b[3]}'
    ), character_a, character_b


@dp.callback_query_handler(lambda c: c.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9'), state=Poll.Polling)
async def get_answer_and_send_next_question(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    # await query.message.edit_text(query.message.text + '\n\nОпа')

    data = await state.get_data()

    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    ratio = 1 / int(query.data) if data.get('inverse', False) else int(query.data)

    answer_pair = (character_a[0], character_b[0], ratio), (character_b[0], character_a[0], 1 / ratio)

    await state.update_data({'answers': data.get('answers') + [*answer_pair]})
    await state.update_data({'current_question': data.get('current_question') + 1})

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        question_text, character_a, character_b = create_question_text(data)
        await query.message.answer(question_text, reply_markup=create_character_choice(character_a[1], character_b[1]))
    else:
        final_text = (f'Опрос окончен. Теперь вам нужно решить, использовать ли ответы в дальнейшем анализе. '
                      f'Если вы вообще не понимали, что вы только что тыкали, то, пожалуйста, выберите "Нет". '
                      f'Если же вы настроены серьезно, то отвечайте "Да".')
        await query.message.answer(final_text, reply_markup=create_analysis_usage_choice())


@dp.callback_query_handler(text='yes', state=Poll.Polling)
@dp.callback_query_handler(text='no', state=Poll.Polling)
async def process_analysis_usage(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    data = await state.get_data()

    analysis_usage = True if query.data == 'yes' and not db.get_user_analysis_usage(query.from_user.id) else False

    poll_information = query.from_user.id, datetime.datetime.today(), analysis_usage

    db.insert_poll_and_answers(poll_information, data.get('answers'))

    await state.finish()


@dp.callback_query_handler(text='stop', state=Poll.Polling)
async def process_stop_poll(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    await query.message.answer('Вы прервали прохождение опроса.')
    await state.finish()


@dp.callback_query_handler(text='cancel', state=Poll.Polling)
async def process_choice_cancel(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    await query.message.edit_reply_markup(reply_markup=create_character_choice(character_a[1], character_b[1]))
