from datetime import datetime
import os

from aiogram import types

import api
import db
import utils
from loader import bot, dp


@dp.message_handler(commands=['start', 'help'])
async def handl_standart_command(message: types.Message) -> None:
    if message.text.lower() == '/start':
        await message.answer("Hi! Please write /help to see all available commands.")
        db.add_user(message.from_user.id)
    elif message.text.lower() == '/help':
        await message.answer("/lst\n/history USD/CAD for 5 days\n/exchange 10 USD to CAD")


@dp.message_handler(commands=['lst', 'history', 'exchange'])
async def handl_exchange_command(message: types.Message) -> None:
    if message.text.lower() == '/lst':
        user = db.get_user(message.from_user.id)
        if utils.check_time_cooldown(user['time']):
            data = api.get_list_currencies(message.from_user.id)
            await message.answer(data)
            db.append_last_request(message.from_user.id, data, datetime.now())
        else:
            await message.answer(user['data'])
    elif message.text.startswith('/history'):
        data = utils.history_command(message.text)
        if isinstance(data, list):
            with open(data[0],"rb") as ph:
                await message.answer_photo(ph, data[1])
            os.remove(data[0])
        else:
            await message.answer(data)
    elif message.text.startswith('/exchange'):
        await message.answer(utils.exchange_command(message.text))
       