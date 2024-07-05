from aiogram.fsm.state import StatesGroup, State


# from aiogram.fsm.storage.redis import RedisStorage


class TypeChatAnswersState(StatesGroup):
    choosing_chat_type_answers = State()
    selected_type_chat_answers = State()


class ChatState(StatesGroup):
    chat_anxiety = State()
    chat_photo = State()
