from service.chat.text import TextChat, ValueTextChat
from service.chat.voice import VoiceChat, ValueVoiceChat


class ChatFactory:

    @staticmethod
    def create_chat(type_answer: str, thread_id: str):
        if type_answer == 'voice':
            return VoiceChat(thread_id)
        elif type_answer == 'text':
            return TextChat(thread_id)
        else:
            raise ValueError(f"Unknown chat type: {type_answer}")