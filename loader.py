import openai
from aiogram import Bot, Dispatcher
from amplitude import Amplitude

from settings import setting


client_openai = openai.AsyncClient(api_key=setting.openai_key)

client_amplitude = Amplitude(api_key=setting.amplitude_api_key)

bot = Bot(token=setting.bot_token)

dp = Dispatcher()
