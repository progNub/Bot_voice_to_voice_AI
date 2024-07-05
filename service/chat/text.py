from aiogram.types import Message

from loader import bot
from service.assistant.assistant import Assistant
from service.assistant.assistantValue import AssistantValue
from service.transcription import get_transcription


class TextChat:
    def __init__(self, thread_id: str):
        self.assistant = AssistantValue(thread_id)

    @staticmethod
    async def _prepare_message(message: Message) -> str:
        text = ''
        if message.content_type == 'voice':
            file_voice = await bot.get_file(message.voice.file_id)
            voice = await bot.download_file(file_voice.file_path)
            text = await get_transcription(voice)
        elif message.content_type == 'text':
            text = message.text
        return text

    async def _prepare_answer(self):
        run = await self.assistant.get_run()
        tread_id = await self.assistant.get_thread_id()

        if run.status == 'completed':
            messages = await (self.assistant.client.beta.threads.messages.
                              list(thread_id=tread_id, limit=1))
            text = messages.data[0].content[0].text.value
            return text
        else:
            return "Sorry I couldn't get answer from server."

    async def send_message(self, message: Message) -> None:
        text = await self._prepare_message(message)
        await self.assistant.create_message(text)
        await self.assistant.do_run()

    async def get_answer(self) -> str:
        text_answer = await self._prepare_answer()
        return text_answer


class ValueTextChat(TextChat):

    def __init__(self, thread_id: str, user_id: int):
        self.user_id = user_id
        super().__init__(thread_id)

    async def send_message(self, message: Message) -> None:
        await super().send_message(message)
        await self.assistant.save_value(self.user_id)
