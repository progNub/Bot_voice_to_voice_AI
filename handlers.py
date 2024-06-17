from aiogram import types, F
from aiogram.filters import CommandStart

from database.models import User
from loader import dp
from service.assistant import Assistant
from service.chat.voice import VoiceChat
from service.utils import registration


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """return information about the bot"""
    information = (f"hello {message.from_user.username}.\n"
                   f"You can ask any question the bot and receive answer from chatGPT")
    if await User.is_user_exists(message.from_user.id) is None:
        await registration(message.from_user.id)

    await message.answer(f"{information} !")


@dp.message(F.content_type.in_({'voice'}))
async def voice_handler(message: types.Message) -> None:
    await message.answer('Please wait, your message is being processed...')

    user = await User.get_user(message.from_user.id)

    if user is None:
        user = await registration(message.from_user.id)

    assistant = Assistant(user.thread_id)
    chat = VoiceChat(assistant)
    await chat.send_message(message.voice)
    voice_answer = await chat.get_answer()

    await message.answer_voice(voice_answer)


@dp.message()
async def voice_handler(message: types.Message) -> None:
    await message.answer(f"I can processing only messages type voice!")
