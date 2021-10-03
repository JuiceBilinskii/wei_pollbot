def create_question_text(data: dict):
    question_text = f'Пара {data.get("current_question") + 1}/{data.get("total_questions")}\n\n'

    first_question = max(data.get("current_question") - 2, 0)
    for question_number in range(first_question, data.get("current_question")):
        character_a, character_b = data.get('characters_combinations')[question_number]
        question_text += f'{question_number + 1}. {character_a["name"]} _____ {character_b["name"]}\n'

    character_a, character_b = data.get('characters_combinations')[data.get("current_question")]
    question_text += f'{data.get("current_question") + 1}. {character_a["name"]} _____ {character_b["name"]} <-\n'

    last_question = min(data.get("current_question") + 3, data.get('total_questions'))
    for question_number in range(data.get("current_question") + 1, last_question):
        character_a, character_b = data.get('characters_combinations')[question_number]
        question_text += f'{question_number + 1}. {character_a["name"]} _____ {character_b["name"]}\n'

    return question_text
