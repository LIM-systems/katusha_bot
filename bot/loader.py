import logging
import pathlib

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from hockey_back.settings import TG_TOKEN

path = pathlib.Path().absolute()
bot = Bot(token=TG_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)