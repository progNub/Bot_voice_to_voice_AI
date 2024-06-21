import io
from abc import ABC, abstractmethod

from service.assistant.assistant import Assistant


class BaseChat(ABC):
    def __init__(self, assistant: Assistant):
        if assistant is None:
            raise ValueError("The assistant must be provided when creating the chat.")
        self.assistant = assistant

    @abstractmethod
    async def send_message(self, message: str | io.BytesIO) -> None:
        pass

    @abstractmethod
    async def get_answer(self) -> str | io.BytesIO:
        pass


