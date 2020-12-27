import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

from parser_kolesa import Kolesa as Parser
from config import TOKEN, ADMIN

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# инициализируем парсер
parser = Parser(admin=ADMIN, bot=bot)


@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
    await message.answer('Привет')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    template = 'Город:Алматы Марка:vaz Пробег:old Кредит:kredit Тип:1 ' \
               'Год_Выпуска_От:2000 Год_Выпуска_До:2020 Цена_От:1000 Цена_До:100000000 Страна:Россия ' \
               'Двигатель:Бензин КПП:Механика'
    await message.reply(f"Введите что-то из списка чтобы увидеть возможные варианты:\n"\
                        f"Марка\nПробег\nСтрана\nКредит\nКузов\nДвигатель\nКПП\nГород\n"\
                        f"Пример запроса:\n{template}")

@dp.message_handler(commands=['clear_cars'])
async def subscribe(message: types.Message):
    parser.links = []
    parser.files = {}
    await message.answer('Список машин успешно очищен')

@dp.message_handler()
async def echo_message(msg: types.Message):
    text = msg.text
    if('/add_car' in text):
        arg = text.split()[1:]
        city = None
        marka = None
        probeg = None
        kredit = None
        type = None
        year_start = None
        year_final = None
        price_start = None
        price_final = None
        country = None
        engine = None
        transmission = None

        print(arg)

        for i in arg:
            i = i.split(':')
            if (i[0] == 'Город'):
                city = i[1]
            elif (i[0] == 'Марка'):
                marka = i[1]
            elif (i[0] == 'Пробег'):
                probeg = i[1]
            elif (i[0] == 'Кредит'):
                kredit = i[1]
            elif (i[0] == 'Тип'):
                type = i[1]
            elif (i[0] == 'Год_Выпуска_От'):
                year_start = i[1]
            elif (i[0] == 'Год_Выпуска_До'):
                year_final = i[1]
            elif (i[0] == 'Цена_От'):
                price_start = i[1]
            elif (i[0] == 'Цена_До'):
                price_final = i[1]
            elif (i[0] == 'Cтрана'):
                country = i[1]
            elif (i[0] == 'Двигатель'):
                engine = i[1]
            elif (i[0] == 'КПП'):
                transmission = i[1]

        c = parser.make_query(city=city, probeg=probeg, marka=marka, kredit=kredit,
                         type=type, year_start=year_start, year_final=year_final,
                         price_start=price_start, price_final=price_final, country=country,
                         engine=engine, transmission=transmission
                         )
        parser.add_car(c)
        await bot.send_message(msg.from_user.id, 'Успешно добавлено')
    elif('/set_views ' in text):
        arg = text.split()[1:]
        try:
            arg = int(arg[0])
            print(arg)
            parser.min_views = arg
            await msg.reply(f'Успешно изменено на {arg}')
        except ValueError:
            await msg.reply('Введите корректное число')
    else:
        keys = parser.print_templates(text)
        if(not keys):
            await msg.reply('Неизвестная команда')
        else:
            answer = ''
            for i in keys:
                answer += f'{i}\n'
            await msg.reply(answer)

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        # проверяем наличие новых машин
        new = parser.parse_cars()
        if(new is not None):
            for i in new:
                for admin in ADMIN:
                    await bot.send_message(admin, i)


# запускаем лонг поллинг
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(5))
    executor.start_polling(dp, loop=loop, skip_updates=True)