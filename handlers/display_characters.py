from aiogram import types
from services.messages_text import create_characters_list_text

from load_all import dp
from services.database_wrapper import select_characters


@dp.message_handler(commands=['display_characters'], state=None)
async def register_user(message: types.Message):
    characters_dict = select_characters()
    characters_list_text = create_characters_list_text(characters_dict.values())
    await message.answer(characters_list_text,
                         disable_web_page_preview=True)
