from aiogram.types import Message

from loader import bot
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
        thread_id = await self.assistant.get_thread_id()

        if run.status == 'completed':
            messages = await self.assistant.client.beta.threads.messages.list(thread_id=thread_id, limit=1)
            message_content = messages.data[0].content[0].text
            annotations = message_content.annotations

            for annotation in annotations:
                if file_citation := getattr(annotation, 'file_citation', None):
                    cited_file = await self.assistant.client.files.retrieve(file_citation.file_id)
                    message_content.value = message_content.value.replace(annotation.text,
                                                                          f'<source: {cited_file.filename}>')
            text = message_content.value
            return text
        else:
            return "Sorry, I couldn't get an answer from the server."

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
