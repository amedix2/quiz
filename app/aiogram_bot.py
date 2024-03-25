import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

__all__ = ['main_bot']

load_dotenv()
AIOGRAM_TOKEN = os.getenv('AIOGRAM_TOKEN')

bot = Bot(token=AIOGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    logging.info(f'process_start_command: {message.chat.id}')
    await bot.send_message(message.chat.id, f'Ты зарегестрировался в системе под именем {message.chat.username}')
    await bot.send_message(message.chat.id, f'Для того чтобы изменить имя используй команду /set новое_имя')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
