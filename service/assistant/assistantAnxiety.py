import logging
from pathlib import Path

from service.assistant.assistant import Assistant

logger = logging.getLogger(__name__)


class AssistantAnxiety(Assistant):

    def __init__(self, file_path="service/assistant/data_for_vectors/anxiety.docx"):
        if not Path(file_path).exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        self.file_path = file_path
        super().__init__()

    async def create_assistant(self):
        initial_data = {'instructions': "You are a competent assistant in matters of anxiety. "
                                        "Use your knowledge base to answer questions about anxiety."
                                        "When using the knowledge base, "
                                        "indicate which file you took the information from",
                        'tools': [{"type": "file_search"}]}

        assistant = await super()._create_assistant(name="Anxiety assistant", **initial_data)
        await self.update_assistant()
        return assistant

    async def create_vector(self, name="About anxiety"):
        vector_store = await self.client.beta.vector_stores.create(name=name)
        return vector_store

    async def update_assistant(self):
        vector_store = await self.create_vector()

        files = (self.file_path.split('/')[-1], open(self.file_path, 'rb'))

        file_batch = await (self.client.beta.vector_stores.file_batches.
                            upload_and_poll(vector_store_id=vector_store.id,
                                            files=[files], poll_interval_ms=self.poll_interval))

        assistant = await self.client.beta.assistants.update(assistant_id=await self.get_assistant_id(),
                                                             tool_resources={"file_search": {
                                                                 "vector_store_ids": [vector_store.id]}}, )

        return assistant
