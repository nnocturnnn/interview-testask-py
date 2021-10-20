import logging

from aiogram import executor, Dispatcher

import db
from loader import dp
import handlers


async def on_startup(dp: Dispatcher) -> None:
    db.init_database()
    logging.basicConfig(level=logging.INFO)

 
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, 
                            skip_updates=False, relax=0.05)