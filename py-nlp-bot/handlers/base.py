from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "This bot can help you check the weather. And describe audio content\n"
        "For any help use /help"
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "If you want to check weather send text message\n\
        In other case send audio file."
    )
