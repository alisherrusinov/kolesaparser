import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

from .parser import Parser
from .config import TOKEN, ADMIN

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# инициализируем парсер
parser = Parser()


# Команда активации подписки
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
    await message.answer('Привет')


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # проверяем наличие новых игр
        new_games = parser

        if (new_games):
            # если игры есть, переворачиваем список и итерируем
            new_games.reverse()
            for ng in new_games:
                # парсим инфу о новой игре
                nfo = sg.game_info(ng)

                # получаем список подписчиков бота
                subscriptions = db.get_subscriptions()

                # отправляем всем новость
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption=nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" +
                                    nfo['link'],
                            disable_notification=True
                        )

                # обновляем ключ
                sg.update_lastkey(nfo['id'])


# запускаем лонг поллинг
if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))  # пока что оставим 10 секунд (в качестве теста)
    executor.start_polling(dp, skip_updates=True)