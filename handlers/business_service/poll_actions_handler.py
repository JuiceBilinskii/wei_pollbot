from aiogram.dispatcher import FSMContext
from .question_text_creation import create_question_text
from .poll_results_calculation import PollResultsCalculator


async def receive_ratio(ratio_choice, state: FSMContext):
    data = await state.get_data()

    character_a, character_b = data.get('characters_combinations')[data.get('current_question')]

    ratio = 1 / int(ratio_choice) if data.get('inverse', False) else int(ratio_choice)

    answer_pair = (character_a['id'], character_b['id'], ratio), (character_b['id'], character_a['id'], 1 / ratio)

    await state.update_data({'answers': data.get('answers') + [*answer_pair]})
    await state.update_data({'current_question': data.get('current_question') + 1})


async def create_next_question(data):
    question_text = create_question_text(data)
    character_a, character_b = data.get('characters_combinations')[data.get("current_question")]
    return question_text, character_a, character_b


async def complete_poll(data, state: FSMContext):
    answers = data.get('answers')
    characters_id = data.get('characters').keys()
    calculator = PollResultsCalculator()
    average_characters_rating, concordance_factor = calculator.calculate_poll_results(answers, characters_id)

    await state.update_data({'average_characters_rating': average_characters_rating,
                             'concordance_factor': concordance_factor})

    message = 'Средние оценки по результатам опроса:\n'
    for character_id, average_rating in average_characters_rating.items():
        message += f'{data.get("characters")[character_id]["name"]}: {average_rating * 100}\n'
    message += f'\nПредварительный коэффициент согласованности: {concordance_factor}\n\n'
    message += (f'Опрос окончен. Теперь вам нужно решить, использовать ли ответы в дальнейшем анализе. '
                f'Если вы вообще не понимали, что вы только что тыкали, то, пожалуйста, выберите "Нет". '
                f'Если же вы настроены серьезно, то отвечайте "Да".')
    return message
