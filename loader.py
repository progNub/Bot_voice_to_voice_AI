import openai
from aiogram import Bot, Dispatcher

from settings import setting


client_openai = openai.AsyncClient(api_key=setting.openai_key)

bot = Bot(setting.bot_token)

dp = Dispatcher()
