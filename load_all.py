from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DatabaseQueriesWrapper
import os


storage = MemoryStorage()

bot = Bot(token=os.environ.get('API_TOKEN'))
dp = Dispatcher(bot, storage=storage)

db = DatabaseQueriesWrapper(host=os.environ.get('host'),
                            database=os.environ.get('database'),
                            user=os.environ.get('user'),
                            password=os.environ.get('password'))
