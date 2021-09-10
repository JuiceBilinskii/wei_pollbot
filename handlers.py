import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from load_all import dp, db

@dp.message_handler(CommandStart())
async def register_user(message: types.Message, state: FSMContext):
    # db.update_user(message.chat.id, 1)
    # await state.update_data({'number_of_replies': 1})
    await message.answer(f'Этот бот предназначен для проведения опроса, результаты которого будут задействованы в дальнейшем анализе.')