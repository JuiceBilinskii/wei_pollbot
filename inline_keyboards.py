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
        ('Равны', '1'),
        (second_character, 'right'),
    )

    row_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return character_choice

def create_ratio_choice():
    ratios = ('3', '5', '7', '9')

    row_buttons = (InlineKeyboardButton(ratio, callback_data=ratio) for ratio in ratios)

    ratio_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return ratio_choice

def create_used_in_analysis_choice():
    names_and_data = (
        ('Использовать в анализе', 'yes'),
        ('Не использовать в анализе', 'no'),
    )

    row_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return character_choice

def create_empty():
    ratio_choice = InlineKeyboardMarkup()
    return ratio_choice
