def create_question_text(data: dict):
    question_text = f'Пара {data.get("current_question") + 1}/{data.get("total_questions")}\n\n'

    question_text += create_text_for_previous_answers(data)

    current_character_a, current_character_b = data.get('characters_combinations')[data.get("current_question")]
    question_text += f'{data.get("current_question") + 1}. {current_character_a["name"]} _____ {current_character_b["name"]} 🟡\n'

    last_question = min(data.get("current_question") + 3, data.get('total_questions'))
    for question_number in range(data.get("current_question") + 1, last_question):
        character_a, character_b = data.get('characters_combinations')[question_number]
        question_text += f'{question_number + 1}. {character_a["name"]} _____ {character_b["name"]} ❌\n'

    question_text += f'\n{current_character_a["short_description"]}\n\n{current_character_b["short_description"]}'

    return question_text


def create_post_poll_question_text(data: dict):
    question_text = f'Пара {data.get("current_question")}/{data.get("total_questions")}\n\n'

    question_text += create_text_for_previous_answers(data)

    return question_text


def create_text_for_previous_answers(data: dict):
    question_text = ''

    first_question = max(data.get("current_question") - 2, 0)
    for question_number in range(first_question, data.get("current_question")):
        character_a, character_b = data.get('characters_combinations')[question_number]

        previous_ratio_text = create_ratio_text_for_previous_answer(len(data.get('characters')),
                                                                    data.get('answers'),
                                                                    question_number)

        question_text += f'{question_number + 1}. {character_a["name"]} {previous_ratio_text} {character_b["name"]} ✅\n'
    return question_text


def create_ratio_text_for_previous_answer(number_of_characters, list_of_answers, question_number):
    answer_index = number_of_characters + question_number * 2
    previous_ratio = list_of_answers[answer_index][2]

    if previous_ratio == 1:
        previous_ratio_text = '<_1_>'
    elif previous_ratio < 1:
        previous_ratio_text = f'<__{int(1 / previous_ratio)}>'
    else:
        previous_ratio_text = f'<{previous_ratio}__>'

    return previous_ratio_text
