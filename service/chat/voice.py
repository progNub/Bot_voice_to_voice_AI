import uuid

from aiogram import types
from aiogram.types import BufferedInputFile

from loader import bot
from service.chat.text import TextChat

from service.transcription import get_transcription, get_voice_from_text


class VoiceChat(TextChat):

    @staticmethod
    async def _prepare_message(message_voice: types.Voice) -> str:
        file_voice = await bot.get_file(message_voice.file_id)
        voice = await bot.download_file(file_voice.file_path)
        text = await get_transcription(voice)
        return text

    async def send_message(self, message_voice: types.Voice) -> None:
        text: str = await self._prepare_message(message_voice)
        await super().send_message(text)

    async def get_answer(self) -> BufferedInputFile:
        text_answer = await super().get_answer()
        voice = await get_voice_from_text(text_answer)
        voice_answer = BufferedInputFile(voice, f'{uuid.uuid4()}-answer-.mp3')
        return voice_answer
