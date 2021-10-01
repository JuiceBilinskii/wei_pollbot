from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DatabaseQueries
import os
import configparser


storage = MemoryStorage()

# config = configparser.ConfigParser()
# config.read('config.ini')

# bot = Bot(token=config['Bot-config']['API_TOKEN'])
bot = Bot(token=os.environ.get('API_TOKEN'))
dp = Dispatcher(bot, storage=storage)

# db_config = config['PostgreSQL']
# db = DatabaseQueries(db_config['host'], db_config['database'], db_config['user'], db_config['password'])
db = DatabaseQueries(host=os.environ.get('host'),
                     database=os.environ.get('database'),
                     user=os.environ.get('user'),
                     password=os.environ.get('password'))
