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
from misc.poll_results_calculator import PollResultsCalculator


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    db.insert_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    start_text = (f'Теперь можете приступить к прохождению опроса. Вам предстоит выполнить ряд '
                  f'попарных сравнений между персонажами на предмет оценки их относительной силы. '
                  f'Подразумевается, что сравнивается не только физическая сила в самом непосредственном '
                  f'смысле, а берется во внимание и ряд других качеств, например, степень влияния '
                  f'персонажа на сюжет.')
    await message.answer(start_text)


@dp.message_handler(commands=['start_poll'], state=None)
async def start_poll(message: types.Message, state: FSMContext):
    # characters_tuple = db.select_characters()
    characters_dict = {character_tuple[0]: {
        'id': character_tuple[0],
        'name': character_tuple[1],
        'height': character_tuple[2],
        'short_description': character_tuple[3],
        'url': character_tuple[4],
    } for character_tuple in db.select_characters()}

    character_combinations = list(combinations(characters_dict.values(), 2))
    random.shuffle(character_combinations)

    await Poll.Polling.set()

    await state.update_data({'characters': characters_dict})
    await state.update_data({'characters_combinations': character_combinations})
    await state.update_data({'current_question': 0})
    await state.update_data({'total_questions': len(character_combinations)})
    await state.update_data({'answers': []})

    await message.answer(f'Количество пар: {len(character_combinations)}')

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        diagonal_answers = []
        for character_id in characters_dict:
            diagonal_answers.append((character_id, character_id, 1))

        await state.update_data({'answers': data.get('answers') + [*diagonal_answers]})

        question_text, character_a, character_b = create_question_text(data)

        await message.answer(question_text,
                             reply_markup=create_character_choice(character_a['name'], character_b['name']))


@dp.callback_query_handler(text='left', state=Poll.Polling)
@dp.callback_query_handler(text='right', state=Poll.Polling)
async def process_character_choice(query: types.CallbackQuery, state: FSMContext):
    message = query.message
    await state.update_data({'inverse': False}) if query.data == 'left' else await state.update_data({'inverse': True})
    await message.edit_reply_markup(reply_markup=create_ratio_choice())


def create_question_text(data):
    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]
    return (
        f'Пара {data.get("current_question") + 1}/{data.get("total_questions")}\n\n'
        f'{character_a["name"]} - {character_a["height"]} см\n'
        f'{character_a["url"]}\n'
        f'{character_a["short_description"]}\n\n'
        f'{character_b["name"]} - {character_b["height"]} см\n'
        f'{character_a["url"]}\n'
        f'{character_b["short_description"]}'
    ), character_a, character_b


@dp.callback_query_handler(lambda c: c.data in ('1', '2', '3', '4', '5', '6', '7', '8', '9'), state=Poll.Polling)
async def get_answer_and_send_next_question(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())

    data = await state.get_data()

    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]

    if data.get('inverse', False):
        ratio = 1 / int(query.data)
        added_text = f'\n_______\nВы выбрали {query.data} в пользу {character_b["name"]}'

    else:
        ratio = int(query.data)
        added_text = f'\n_______\nВы выбрали {query.data} в пользу {character_a["name"]}'

    previous_message_text = query.message.text + added_text

    await query.message.edit_text(previous_message_text)

    answer_pair = (character_a['id'], character_b['id'], ratio), (character_b['id'], character_a['id'], 1 / ratio)

    await state.update_data({'answers': data.get('answers') + [*answer_pair]})
    await state.update_data({'current_question': data.get('current_question') + 1})

    data = await state.get_data()
    if data.get('current_question') < data.get('total_questions'):
        question_text, character_a, character_b = create_question_text(data)
        await query.message.answer(question_text,
                                   reply_markup=create_character_choice(character_a['name'], character_b['name']))
    else:
        answers = data.get('answers')
        characters_id = data.get('characters').keys()
        calculator = PollResultsCalculator()
        average_characters_rating, concordance_factor = calculator.average_characters_rating_and_concordance_factor(
            answers,
            characters_id)

        await state.update_data({'average_characters_rating': average_characters_rating,
                                 'concordance_factor': concordance_factor})

        message = 'Средние оценки по результатам опроса:\n'
        for character_id, average_rating in average_characters_rating.items():
            message += f'{data.get("characters")[character_id]["name"]}: {average_rating * 100}\n'
        message += f'\nПредварительный коэффициент согласованности: {concordance_factor}\n\n'
        message += (f'Опрос окончен. Теперь вам нужно решить, использовать ли ответы в дальнейшем анализе. '
                    f'Если вы вообще не понимали, что вы только что тыкали, то, пожалуйста, выберите "Нет". '
                    f'Если же вы настроены серьезно, то отвечайте "Да".')
        await query.message.answer(message, reply_markup=create_analysis_usage_choice())


@dp.callback_query_handler(text='yes', state=Poll.Polling)
@dp.callback_query_handler(text='no', state=Poll.Polling)
async def process_analysis_usage(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_reply_markup(reply_markup=create_empty())
    data = await state.get_data()

    analysis_usage = True if query.data == 'yes' and not db.get_user_analysis_usage(query.from_user.id) else False

    poll_information = query.from_user.id, datetime.datetime.today(), analysis_usage, data.get('concordance_factor')

    db.insert_poll_answers_and_rating(poll_information, data.get('answers'), data.get('average_characters_rating'))

    await query.message.answer('Спасибо за участие в опросе.')
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
