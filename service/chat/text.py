from service.assistant.assistantValue import AssistantValue
from service.chat.base import BaseChat


class TextChat(BaseChat):

    async def _prepare_answer(self):
        run = await self.assistant.get_run()
        tread_id = await self.assistant.get_thread_id()

        if run.status == 'completed':
            messages = await (self.assistant.client.beta.threads.messages.
                              list(thread_id=tread_id, limit=1))

            return messages.data[0].content[0].text.value
        else:
            return "Sorry I couldn't get answer from server."

    async def send_message(self, message: str) -> None:
        await self.assistant.create_message(message)
        await self.assistant.do_run()

    async def get_answer(self) -> str:
        text_answer = await self._prepare_answer()
        return text_answer


class ValueTextChat(TextChat):
    def __init__(self, assistant: AssistantValue, user_id: int):
        self.user_id = user_id
        super().__init__(assistant)

    async def send_message(self, message: str) -> None:
        await super().send_message(message)
        await self.assistant.save_value(self.user_id)
