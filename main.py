import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN, PROXY_URL, PROXY_AUTH
from model import Net

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
style_model = Net(ngf=128)


if __name__ == "__main__":
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)