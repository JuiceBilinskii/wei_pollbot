def create_question_text(data: dict):
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
