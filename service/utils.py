from database.models import User
from service.assistant.assistantValue import AssistantValue


async def registration(telegram_id):
    assistant = await AssistantValue().initialize()
    thread_id = await assistant.get_thread_id()
    user = await User(telegram_id=telegram_id, thread_id=thread_id).save()
    return user
