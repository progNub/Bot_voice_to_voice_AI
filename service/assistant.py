from loader import client_openai
from settings import setting


class Assistant:

    def __init__(self, thread_id=None, assistant_id=setting.assistant_key, client=client_openai):
        self.client = client
        self._assistant_id = assistant_id
        self._thread_id = thread_id

        self._assistant = None
        self._thread = None
        self._message = None
        self._run = None

    async def initialize(self):
        await self._create_thread()
        return self

    async def _create_assistant(self, model="gpt-4o", name="Mr Smith"):
        self._assistant = await self.client.beta.assistants.create(model=model, name=name)
        return self._assistant

    async def _create_thread(self):
        self._thread = await self.client.beta.threads.create()
        return self._thread

    async def _create_message(self, message):
        if message is not None:
            self._message = await (self.client.beta.threads.messages.
                                   create(thread_id=await self.get_thread_id(), role="user", content=message))

            return self._message

    async def _do_run(self):
        self._run = await (self.client.beta.threads.runs.
                           create_and_poll(thread_id=await self.get_thread_id(),
                                           assistant_id=await self.get_assistant_id()))

        return self._run

    async def get_assistant_id(self):
        if self._assistant_id is None:
            return self._assistant.id
        return self._assistant_id

    async def get_thread_id(self):
        if self._thread is None:
            return self._thread_id
        return self._thread.id

    async def get_answer_messages(self):
        if self._run.status == 'completed':
            messages = await self.client.beta.threads.messages.list(thread_id=await self.get_thread_id(), limit=1)
            return messages

    async def get_last_answer(self) -> str:
        last_message = await self.get_answer_messages()
        text = last_message.data[0].content[0].text.value
        return text

    async def send_message(self, question: str):
        await self._create_message(question)
        await self._do_run()
