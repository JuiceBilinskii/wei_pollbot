from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from load_all import dp
from services.database_wrapper import register_user
from services.messages_text import create_start_poll_text


@dp.message_handler(CommandStart())
async def handle_start_command(message: types.Message):
    """Handles '/start' command. Registers new user and sends response text."""

    await register_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(create_start_poll_text())
