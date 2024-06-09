from aiogram import types, F

from aiogram.filters import CommandStart

from aiogram.types.input_file import BufferedInputFile

from database.models import User
from loader import dp, bot
from service.assistant import Assistant
from service.transcription import get_transcription, get_voice_from_text


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """return information about the bot"""
    information = (f"hello {message.from_user.username}.\n"
                   f"You can ask any question the bot and receive answer from chatGPT")
    if await User.is_user_exists(message.from_user.id) is None:
        assistant = await Assistant().initialize()
        assistant_id = await assistant.get_assistant_id()
        thread_id = await assistant.get_thread_id()
        telegram_id = message.from_user.id
        user = User(telegram_id=telegram_id, assistant_id=assistant_id, thread_id=thread_id)
        await user.save()

    await message.answer(f"{information} !")


@dp.message(F.content_type.in_({'voice'}))
async def voice_handler(message: types.Message) -> None:
    await message.answer('Please wait, your message is being processed...')

    user = await User.get_user(message.from_user.id)
    assistant = Assistant(user.assistant_id, user.thread_id)

    file = await bot.get_file(message.voice.file_id)

    voice = await bot.download_file(file.file_path)

    text = await get_transcription(voice)

    await assistant.send_message(text)

    text = await assistant.get_last_answer()

    voice_gpt = await get_voice_from_text(text)

    output_voice = BufferedInputFile(voice_gpt, 'answer.mp3')

    await message.answer_voice(output_voice)


@dp.message()
async def voice_handler(message: types.Message) -> None:
    await message.answer(f"I can processing only messages type voice!")
