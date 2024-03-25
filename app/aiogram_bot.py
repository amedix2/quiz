import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv()
TOKEN = os.getenv('AIOGRAM_TOKEN')

dp = Dispatcher()

__all__ = ['main']


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info(f'started by {message.chat.id}')
    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!\n'
                         f'Ты был зарегестрирован в системе под именем'
                         f' {hbold(message.from_user.username)}')
    await message.answer(f'Для смены имени используй команду\n/set новое_имя')


@dp.message(F.text, Command('set'))
async def command_set_handler(message: Message) -> None:
    logging.info(f'set name by {message.chat.id}')
    name = message.text[5:].strip()
    if name:
        await message.answer(f'Ты изменил имя на {hbold(name)}')
    else:
        await message.answer(f'Нельзя использовать пустое имя!')


@dp.message(F.text, Command('help'))
async def command_set_handler(message: Message) -> None:
    logging.info(f'help by {message.chat.id}')
    await message.answer('Пиши ответы (a, b, c или d) на вопрос, который видишь на экране\n\n'
                         'Используй /set имя для смены имени(пожалуйста не'
                         ' используйте это во время вопроса я не знаю что произойдет-_-)')


@dp.message()
async def answers_handler(message: types.Message) -> None:
    logging.info(f'answer by {message.chat.id}')
    try:
        if message.text.lower() in ('a', 'b', 'c', 'd'):
            await message.answer(f'Ответ {hbold(message.text)} был принят!')
        else:
            await message.answer(f'Такого варианта ответа нет((\n'
                                 f'Выбери что то другое из предложенного')
    except Exception:
        await message.answer('Зевс тобой не доволен!!!')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
