from service.chat.base import BaseChat


class TextChat(BaseChat):

    async def _get_answer_messages(self):
        run = await self.assistant.get_run()
        tread_id = await self.assistant.get_thread_id()
        if run.status == 'completed':
            messages = await (self.assistant.client.beta.threads.messages.
                              list(thread_id=tread_id, limit=1))

            return messages.data[0].content[0].text.value

    async def send_message(self, message: str) -> None:
        await self.assistant.create_message(message)
        await self.assistant.do_run()

    async def get_answer(self) -> str:
        text_answer = await self._get_answer_messages()
        return text_answer
