import json
import os

from aiogram import F, Router
from aiogram.types import Message

from utils.describe import transcribe_audio
from utils.llm import chat_completion_request, functions, messages
from utils.misc import execute_function_call, get_natural_response

router = Router()


@router.message(F.audio | F.voice)
async def convert_audio(message: Message):
    filename = "audio.mp3"
    if message.audio:
        await message.bot.download(message.audio, destination=filename)
    elif message.voice:
        await message.bot.download(message.voice, destination=filename)
    await message.reply(await transcribe_audio())
    try:
        os.remove(filename)
        print(f"File '{filename}' has been successfully removed.")
    except OSError as e:
        print(f"Error: {e}")


@router.message()
async def check_weather(message: Message):
    user_message = message.text
    messages.append({"role": "user", "content": user_message})
    chat_response = chat_completion_request(messages=messages,
                                            functions=functions)
    assistant_message = chat_response.json()["choices"][0]["message"]
    results = execute_function_call(assistant_message)
    content = json.dumps(results)
    content = get_natural_response(content, message.text)
    await message.reply(content)
