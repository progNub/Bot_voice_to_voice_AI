from database.models import User
from service.assistant import Assistant


async def registration(telegram_id):
    assistant = await Assistant().initialize()
    assistant_id = await assistant.get_assistant_id()
    thread_id = await assistant.get_thread_id()
    user = await User(telegram_id=telegram_id, assistant_id=assistant_id, thread_id=thread_id).save()
    return user
