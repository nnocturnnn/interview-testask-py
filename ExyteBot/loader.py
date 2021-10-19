import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)