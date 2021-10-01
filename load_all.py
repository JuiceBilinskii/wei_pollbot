from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DatabaseQueries
import os
import configparser


storage = MemoryStorage()

config = configparser.ConfigParser()
config.read('config.ini')

# bot = Bot(token=config['Bot-config']['API_TOKEN'])
bot = Bot(token=os.environ['API_TOKEN'])
dp = Dispatcher(bot, storage=storage)

db_config = config['PostgreSQL']
# db = DatabaseQueries(db_config['host'], db_config['database'], db_config['user'], db_config['password'])
db = DatabaseQueries(host=os.environ['host'],
                     database=os.environ['database'],
                     user=os.environ['user'],
                     password=os.environ['password'])
