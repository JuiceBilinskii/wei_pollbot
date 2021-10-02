from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from load_all import dp, db


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    db.insert_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    start_text = (f'Теперь можете приступить к прохождению опроса. Вам предстоит выполнить ряд '
                  f'попарных сравнений между персонажами на предмет оценки их относительной силы. '
                  f'Подразумевается, что сравнивается не только физическая сила в самом непосредственном '
                  f'смысле, а берется во внимание и ряд других качеств, например, степень влияния '
                  f'персонажа на сюжет.')
    await message.answer(start_text)
