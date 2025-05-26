import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
import redis
import datetime

API_TOKEN = 'ВАШ ТОКЕН'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

r = redis.Redis(host='localhost', port=6379, db=0)

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}.")

@dp.message(Command("ping"))
async def ping(message: types.Message):
    user_id = str(message.from_user.id)
    r.incr(f'ping_count:{user_id}')
    await message.answer("pong")

@dp.message(Command("ping/my"))
async def ping_count_output(message: types.Message):
    user_id = str(message.from_user.id)
    ping_count = r.get(f'ping_count:{user_id}')
    if ping_count is not None:
        await message.answer(ping_count.decode())
    else:
        await message.answer("Вы еще не использовали команду /ping.")

@dp.message(Command("time"))
async def send_current_time(message: types.Message):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    await message.answer(f"Текущее время: {formatted_time}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
