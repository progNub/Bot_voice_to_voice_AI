from aiogram import types, F

from aiogram.filters import CommandStart

from aiogram.types.input_file import BufferedInputFile

from loader import dp, bot
from service.assistant import assistant
from service.transcription import get_transcription, get_voice_from_text


@dp.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    """return information about the bot"""
    information = (f"hello {message.from_user.username}.\n"
                   f"You can ask any question the bot and receive answer from chatGPT")
    await message.answer(f"{information} !")


@dp.message(F.content_type.in_({'voice'}))
async def voice_handler(message: types.Message) -> None:
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
