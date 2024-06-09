import asyncio

from loader import client_openai


class Assistant:

    def __init__(self, client=client_openai, assistant=None, thread=None):
        self.client = client
        self._assistant = assistant
        self._thread = thread
        self._message = None
        self._run = None

    async def initialize(self):
        await self.create_assistant()
        await self.create_thread()
        return self

    async def create_assistant(self, model="gpt-4o", name="Mr Smith"):
        self._assistant = await self.client.beta.assistants.create(model=model, name=name)
        return self._assistant

    async def create_thread(self):
        self._thread = await self.client.beta.threads.create()
        return self._thread

    async def create_message(self, message):
        if message is not None:
            self._message = await (self.client.beta.threads.messages.
                                   create(thread_id=self._thread.id, role="user", content=message))

            return self._message
        else:
            raise Exception("Message can't be empty.")

    async def do_run(self):
        self._run = await (self.client.beta.threads.runs.
                           create_and_poll(thread_id=self._thread.id, assistant_id=self._assistant.id))

        return self._run

    async def get_answer_messages(self):
        if self._run.status == 'completed':
            messages = await self.client.beta.threads.messages.list(thread_id=self._thread.id, limit=1)
            return messages
        return

    async def get_last_answer(self) -> str:
        last_message = await self.get_answer_messages()
        text = last_message.data[0].content[0].text.value
        return text

    async def send_message(self, question: str):
        await self.create_message(question)
        await self.do_run()


assistant = asyncio.run(Assistant().initialize())
