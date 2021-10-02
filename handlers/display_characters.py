from aiogram import types
from utils.characters_list_creator import create_characters_list_message

from load_all import dp, db


@dp.message_handler(commands=['display_characters'], state=None)
async def register_user(message: types.Message):
    characters_dict = db.select_characters()
    message_text = create_characters_list_message(characters_dict.values())
    await message.answer(message_text, disable_web_page_preview=True)
