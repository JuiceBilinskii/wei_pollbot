from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_character_choice(first_character, second_character):
    names_and_data = (
        (first_character, 'A'),
        ('Равны', '1'),
        (second_character, 'B'),
    )

    row_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in names_and_data)

    character_choice = InlineKeyboardMarkup(inline_keyboard=[[*row_buttons]])
    return character_choice

choose_ratio = InlineKeyboardMarkup(
    inline_keyboard=[
        InlineKeyboardButton('1'),
        InlineKeyboardButton('3'),
        InlineKeyboardButton('5'),
        InlineKeyboardButton('7'),
        InlineKeyboardButton('9'),
    ]
)