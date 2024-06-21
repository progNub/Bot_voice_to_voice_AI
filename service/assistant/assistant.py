from openai.types.beta.threads import Run

from loader import client_openai
from settings import setting


class Assistant:
    poll_interval = 3 * 1000

    def __init__(self, thread_id=None, assistant_id=setting.assistant_key, client=client_openai):
        self._run: Run = None
        self.client = client
        self._assistant_id = assistant_id
        self._thread_id = thread_id
        self._message_id = None

    async def initialize(self):
        await self.create_thread()
        return self

    async def _create_assistant(self, model="gpt-4o", name="Mr Smith", **kwargs):
        assistant = await self.client.beta.assistants.create(model=model, name=name, **kwargs)
        self._assistant_id = assistant.id
        return assistant

    async def create_thread(self):
        thread = await self.client.beta.threads.create()
        self._thread_id = thread.id
        return thread

    async def create_message(self, message):
        if message is not None:
            message = await (self.client.beta.threads.messages.
                             create(thread_id=await self.get_thread_id(), role="user", content=message))
            self._message_id = message.id
            return message

    async def do_run(self) -> Run:
        self._run = await (self.client.beta.threads.runs.
                           create_and_poll(thread_id=await self.get_thread_id(),
                                           assistant_id=await self.get_assistant_id(),
                                           poll_interval_ms=self.poll_interval))

        return self._run

    async def get_run(self) -> Run:
        self._run = await (self.client.beta.threads.runs.
                           retrieve(thread_id=await self.get_thread_id(), run_id=self._run.id))
        return self._run

    async def get_assistant_id(self):
        return self._assistant_id

    async def get_thread_id(self):
        return self._thread_id

