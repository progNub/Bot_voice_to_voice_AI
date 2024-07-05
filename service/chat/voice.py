import uuid

from aiogram.types import BufferedInputFile, Message

from service.assistant.assistantValue import AssistantValue
from service.chat.text import TextChat
from service.transcription import get_voice_from_text


class VoiceChat(TextChat):

    async def _prepare_answer(self) -> BufferedInputFile:
        text_answer = await super()._prepare_answer()

        voice = await get_voice_from_text(text_answer)
        voice_answer = BufferedInputFile(voice, f'{uuid.uuid4()}-answer-.mp3')
        return voice_answer


class ValueVoiceChat(VoiceChat):

    def __init__(self, thread_id: str, user_id: int):
        self.user_id = user_id
        super().__init__(thread_id)

    async def send_message(self, message: Message) -> None:
        await super().send_message(message)
        await self.assistant.save_value(self.user_id)
