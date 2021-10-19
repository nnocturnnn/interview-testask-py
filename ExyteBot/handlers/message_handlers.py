from aiogram import types

from loader import bot, dp
from utils import check_time_cooldown
import db
import api


@dp.message_handler(commands=['start', 'help'])
async def handl_admin_command(message: types.Message) -> None:
    if message.text.lower() == '/start':
        db.add_user(message.from_user.id)
    elif message.text.lower() == '/help':
        await message.answer("/lst\n/history USD/CAD\n/exchange 10 USD to CAD")


@dp.message_handler(commands=['lst', 'history', 'exchange'])
async def handl_exchange_command(message: types.Message) -> None:
    if message.text.lower() == '/lst':
        user = db.get_user(message.from_user.id)
        if check_time_cooldown(user['time']):
            message.answer(api.get_list_currencies(message.from_user.id))
        else:
            message.answer(user['data'])
    elif message.text.startswith('/history'):
        pass
    elif message.text.startswith('/exchange'):
        pass
    else:
        await message.answer(f"Sorry, illegal command {message.text}.\n\
Please write /help to see all available commands.")