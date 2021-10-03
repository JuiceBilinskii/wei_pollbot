from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_start_choice():
    names_and_data = (
        ('Начать опрос', 'start'),
    )

    row_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return character_choice


def create_character_choice(first_character, second_character):
    names_and_data = (
        (first_character, 'left'),
        (second_character, 'right'),
    )
    equal = ('Равны', '1')
    terminate = ('Прервать', 'stop')

    first_row = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)
    second_row = InlineKeyboardButton(equal[0], callback_data=equal[1])
    third_row = InlineKeyboardButton(terminate[0], callback_data=terminate[1])

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*first_row], [second_row], [third_row]])
    return character_choice


def create_ratio_choice():
    ratios = ('2', '3', '4', '5'), ('6', '7', '8', '9')
    cancel = ('Отменить', 'cancel')

    first_row = (InlineKeyboardButton(ratio, callback_data=ratio) for ratio in ratios[0])
    second_row = (InlineKeyboardButton(ratio, callback_data=ratio) for ratio in ratios[1])
    third_row = InlineKeyboardButton(cancel[0], callback_data=cancel[1])

    ratio_choice = InlineKeyboardMarkup(inline_keyboard=[[*first_row], [*second_row], [third_row]])
    return ratio_choice


def create_analysis_usage_choice():
    names_and_data = (
        ('Да', 'yes'),
        ('Нет', 'no'),
    )

    row_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return character_choice


def create_empty():
    ratio_choice = InlineKeyboardMarkup()
    return ratio_choice
