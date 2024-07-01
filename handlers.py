from aiogram import types, F
from aiogram.filters import CommandStart

from database.models import User
from loader import dp
from service.vision import Vision
from service.assistant.assistantValue import AssistantValue
from service.chat.text import ValueTextChat
from service.chat.voice import VoiceChat
from service.registration import registration


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """return information about the bot"""
    if await User.get_object_or_none(telegram_id=message.from_user.id) is None:
        await registration(message.from_user.id)

    information = (f"hello {message.from_user.username}.\n"
                   f"You can ask any question the bot and receive answer from chatGPT")
    await message.answer(f"{information} !")


@dp.message(F.content_type.in_({types.ContentType.VOICE}))
async def voice_handler(message: types.Message) -> None:
    await message.answer('Please wait, your message is being processed...')

    user = await User.get_object_or_none(telegram_id=message.from_user.id)
    if user is None:
        user = await registration(message.from_user.id)

    assistant = AssistantValue(user.thread_id)
    chat = VoiceChat(assistant, message.from_user.id)
    await chat.send_message(message.voice)
    voice_answer = await chat.get_answer()

    await message.reply_voice(voice_answer)


@dp.message((F.content_type.in_({types.ContentType.TEXT})))
async def text_handler(message: types.Message) -> None:
    user = await User.get_object_or_none(telegram_id=message.from_user.id)
    if user is None:
        user = await registration(message.from_user.id)

    assistant = AssistantValue(user.thread_id)
    chat = ValueTextChat(assistant, message.from_user.id)
    await chat.send_message(message.text)
    answer = await chat.get_answer()
    if answer:
        await message.reply(answer)


@dp.message((F.content_type.in_({types.ContentType.PHOTO})))
async def text_handler(message: types.Message) -> None:
    await message.answer('Please wait, your message is being processed...')
    vision = Vision(message.photo)
    answer = await vision.analise_emotions()
    await message.reply(answer)


@dp.message()
async def other_message_handler(message: types.Message) -> None:
    await message.answer("Sorry, I can process text, voice and photo messages.")
