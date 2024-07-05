import atexit
from concurrent.futures import ThreadPoolExecutor

import openai
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from amplitude import Amplitude

from settings import setting

client_openai = openai.AsyncClient(api_key=setting.openai_key)

client_amplitude = Amplitude(api_key=setting.amplitude_api_key)

bot = Bot(token=setting.bot_token)

thread_executor = ThreadPoolExecutor(max_workers=5)
atexit.register(lambda: thread_executor.shutdown(wait=True))


redis_storage = RedisStorage.from_url(url=setting.redis_storage_url)
dp = Dispatcher(storage=redis_storage)
