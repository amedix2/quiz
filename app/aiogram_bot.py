import asyncio
import logging
import os
import sys
import json
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
    id = ("id" + str(message.chat.id))
    data = json.load(open('data/players.json', 'r'))
    if id not in data.keys():
        data[id] = {'nickname': message.chat.username, 'score': 0}
    logging.error(data)
    player_name = data[id]['nickname']
    open('data/players.json', 'w').write(json.dumps(data))

    await message.answer(f'Привет, {hbold(message.from_user.full_name)}!\n'
                         f'Ты зарегестрирован в системе под именем'
                         f' {hbold(player_name)}')
    await message.answer(f'Для смены имени используй команду\n/set новое_имя')


@dp.message(F.text, Command('set'))
async def command_set_handler(message: Message) -> None:
    logging.info(f'set name by {message.chat.id}')
    name = message.text[5:].strip()
    id = ("id" + str(message.chat.id))
    data = json.load(open('data/players.json', 'r'))
    data[id]['nickname'] = name
    player_name = data[id]['nickname']
    open('data/players.json', 'w').write(json.dumps(data))
    if name:
        await message.answer(f'Ты изменил имя на {hbold(player_name)}')
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
        answer = message.text.lower()
        if answer in ('a', 'b', 'c', 'd'):
            id = ("id" + str(message.chat.id))
            questions_info = json.load(open('data/questions.json', 'r'))
            data = json.load(open('data/players.json', 'r'))
            if questions_info[questions_info['current']]['right_answer_id'] == answer:
                data[id]['score'] += 1000
            open('data/players.json', 'w').write(json.dumps(data))
            await message.answer(f'Ответ {hbold(message.text)} был принят!')
            logging.error('AAAAAAAAAAAAAAAA')
        else:
            await message.answer(f'Такого варианта ответа нет((\n'
                                 f'Выбери что то другое из предложенного')
    except TypeError or AttributeError:
        await message.answer('Зевс тобой не доволен!!!')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
