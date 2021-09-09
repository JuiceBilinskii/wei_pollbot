from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DatabaseQuiries
import configparser


storage = MemoryStorage()

config = configparser.ConfigParser()
config.read('config.ini')

bot = Bot(token=config['Bot-config']['API_TOKEN'])
dp = Dispatcher(bot, storage=storage)

db_config = config['PostgreSQL']
db = DatabaseQuiries(db_config['host'], db_config['database'], db_config['user'], db_config['password'])
