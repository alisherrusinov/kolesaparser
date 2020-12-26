from bs4 import BeautifulSoup
import requests
import json
import os


# https://kolesa.kz/cars/avtomobili-s-probegom/avtokredit/nissan/almaty/?auto-car-grbody=2&year[from]=2004&year[
# to]=2020&price[from]=1%20000&price[to]=100%20000%20000
# https://kolesa.kz/cars/PROBEG/KREDIT/MARKA/CITY/
class Parser:
    def __init__(self):
        self.probegs = {
            'old': 'avtomobili-s-probegom',
            'new': 'novye-avtomobili'
        }
        self.kredit = {
            'kredit': 'avtokredit',
        }
        self.marks = {
            'audi': 'audi',
            'bmw': 'bmw',
            'cadillac': 'cadillac',
            'chery': 'chery',
            'chevrolet': 'chevrolet',
            'chrysler': 'chrysler',
            'citroen': 'citroen',
            'daewoo': 'daewoo',
            'datsun': 'datsun',
            'dodge': 'dodge',
            'faw': 'faw',
            'fiat': 'fiat',
            'ford': 'ford',
            'geely': 'geely',
            'great-wall': 'great-wall',
            'honda': 'honda',
            'hummer': 'hummer',
            'hyundai': 'hyundai',
            'isuzu': 'isuzu',
            'jac': 'jac',
            'jaguar': 'jaguar',
            'jeep': 'jeep',
            'kia': 'kia',
            'land-rover': 'land-rover',
            'lexus': 'lexus',
            'lifan': 'lifan',
            'lincoln': 'lincoln',
            'mazda': 'mazda',
            'mercedes-benz': 'mercedes-benz',
            'mini': 'mini',
            'mitsubishi': 'mitsubishi',
            'nissan': 'nissan',
            'opel': 'opel',
            'peugeot': 'peugeot',
            'ravon': 'ravon',
            'renault': 'renault',
            'skoda': 'skoda',
            'ssang-yong': 'ssang-yong',
            'subaru': 'subaru',
            'suzuki': 'suzuki',
            'toyota': 'toyota',
            'volkswagen': 'volkswagen',
            'volvo': 'volvo',
            'vaz': 'vaz',
            'gaz': 'gaz',
            'zaz': 'zaz',
            'ij': 'ij',
            'moskvich': 'moskvich',
            'retro-automobiles': 'retro-automobiles',
            'uaz': 'uaz',
            'uaz': 'uaz',
        }

        self.cities = {
            'актау': 'aktau',
            'актобе': 'aktobe',
            'алматы': 'almaty',
            'атырау': 'atyrau',
            'жезказган': 'atyrau',
        }

        self.types = {
            1: 'auto-car-grbody=1',
            2: 'auto-car-grbody=2',
            3: 'auto-car-grbody=3'
        }# auto-car-grbody

        self.countries = {
            'Англия':'1',
            'Германия':'2',
            'Италия':'3',
            'Испания':'4',
            'Франция':'5',
            'Чехия':'6',
            'Швеция':'7',
            'Китай':'8',
            'Южная Корея':'9',
            'Россия':'10',
            'США':'11',
            'Япония':'12',
            'Другие страны':'13',
            'Европа':'14',
        }# mark-country

        self.kuzovs = {
            'Седан':'sedan',
            'Универсал':'station-wagon',
            'Хэтчбек':'hatchback',
            'Лимузин':'limousine',
            'Купе':'body-coupe',
            'Родстер':'body-roadster',
            'Кабриолет':'cabriolet',
            'Внедорождник':'suv',
            'Кроссовер':'crossover-suv',
            'Микровен':'microvan',
            'Минивен':'minivan',
            'Микроавтобус':'van',
            'Фургон':'wagon',
            'Пикап':'body-pickup',
            'Тарга':'targa',
            'Фастбек':'fastback',
            'Лифтбек':'liftback',
            'Хардтоп':'hardtop',
        }

        self.engines = {
            'Бензин':'1',
            'Дизель':'2',
            'Газ-бензин':'3',
            'Газ':'4',
            'Гибрид':'5',
            'Электричество':'6',
        } # auto-fuel

        self.transms = {
            'Механика':'1',
            'АКПП':'2345',
            'Автомат':'2',
            'Типтроник':'3',
            'Вариатор':'4',
            'Робот':'5',
        } # auto-car-transm

        self.ruls = {
            'Слева':'1',
            'Справа':'2',
        } # auto-sweel

        self.privods = {
            'Передний':'1',
            'Задний':'3',
            'Полный':'2',
        } # car-dwheel

        self.links = []
        self.files = {}
        # https://kolesa.kz/cars/avtomobili-s-probegom/sedan/avtokredit/vaz/almaty/
        # ?auto-car-grbody=1
        # &mark-country=10
        # &auto-fuel=1
        # &auto-car-transm=2
        # &auto-sweel=1&car-dwheel=1
        # &auto-run[to]=10000000
        # &auto-car-order=1
        # &auto-car-volume[from]=1
        # &auto-car-volume[to]=10
        # &auto-color=5
        # &year[from]=2010
        # &year[to]=2020
        # &price[from]=120000
        # &price[to]=1002000020000

    def make_query(self, city=None, marka=None, probeg=None, kredit=None, type=1, year_start=None, year_final=None,
                   price_start=None, price_final=None):
        url = 'https://kolesa.kz/cars/'

        if (probeg is not None):
            url += f'{self.probegs[probeg]}/'
        if (kredit is not None):
            url += f'{self.kredit[kredit]}/'
        if (marka is not None):
            url += f'{self.marks[marka]}/'
        if (city is not None):
            url += f'{self.cities[city]}/'
        if (type is not None):
            url += f'?{self.types[type]}'
        if (year_start is not None):
            url += f'&year[from]={year_start}'
        if (year_final is not None):
            url += f'&year[to]={year_final}'
        if (price_start is not None):
            url += f'&price[from]={price_start}'
        if (price_final is not None):
            url += f'&price[to]={price_final}'
        return url

    def add_car(self, url):
        self.links.append(url)
        req = requests.get(url)
        if (req.status_code != 200):
            print('Ошибка при запросе')
            return False
        parser = BeautifulSoup(req.text, 'lxml')

        # ПОЛУЧЕНИЕ БЕЛЫХ БЛОКОВ(БЕЗ ВСЯКИХ БУСТОВ)
        list_blocks = parser.find_all('div', {'class': 'row vw-item list-item a-elem'})
        spans = []  # Список штучек с заголовком объявления
        for th in list_blocks:
            spans.extend(th.find_all('span', {'class': 'a-el-info-title'}))  # Получение штучек с заголовком объявления
        result = []  # Список с тегами а(ссылка в html)
        for th in spans:
            result.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id': 'main'}))
        links = []  # Конечный список самих ссылок

        for i in result:
            link = i['href']
            links.append(f'https://kolesa.kz{link}')

        # ПОЛУЧЕНИЕ ГОЛУБЫХ БЛОКОВ(БУСТЫ ЕСТЬ, НО ПРОСМОТРОВ ТОЖЕ НЕМНОГО)
        list_blocks = parser.find_all('div', {'class': 'row vw-item list-item blue a-elem'})
        spans = []  # Список штучек с заголовком объявления
        for th in list_blocks:
            spans.extend(th.find_all('span', {'class': 'a-el-info-title'}))  # Получение штучек с заголовком объявления
        result = []  # Список с тегами а(ссылка в html)
        for th in spans:
            result.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id': 'main'}))

        for i in result:
            link = i['href']
            links.append(f'https://kolesa.kz{link}')

        print('вывод', links)
        self.files[url] = f'{len(self.links)}.json'
        with open(self.files[url], "w") as write_file:
            json.dump(links, write_file)

    def parse_cars(self):
        for url in self.links:
            with open(self.files[url], "r") as read_file:
                database = json.load(read_file)
            read_file.close()
            req = requests.get(url)
            if (req.status_code == 404):
                print('Неверная ссылка')
                return False
            parser = BeautifulSoup(req.text, 'lxml')

            # ПОЛУЧЕНИЕ БЕЛЫХ БЛОКОВ(БЕЗ ВСЯКИХ БУСТОВ)
            list_blocks = parser.find_all('div', {'class': 'row vw-item list-item a-elem'})
            spans = []  # Список штучек с заголовком объявления
            for th in list_blocks:
                spans.extend(
                    th.find_all('span', {'class': 'a-el-info-title'}))  # Получение штучек с заголовком объявления
            result = []  # Список с тегами а(ссылка в html)
            for th in spans:
                result.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id': 'main'}))
            links = []  # Конечный список самих ссылок

            for i in result:
                link = i['href']
                links.append(f'https://kolesa.kz{link}')

            # ПОЛУЧЕНИЕ ГОЛУБЫХ БЛОКОВ(БУСТЫ ЕСТЬ, НО ПРОСМОТРОВ ТОЖЕ НЕМНОГО)
            list_blocks = parser.find_all('div', {'class': 'row vw-item list-item blue a-elem'})
            spans = []  # Список штучек с заголовком объявления
            for th in list_blocks:
                spans.extend(
                    th.find_all('span', {'class': 'a-el-info-title'}))  # Получение штучек с заголовком объявления
            result = []  # Список с тегами а(ссылка в html)
            for th in spans:
                result.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id': 'main'}))

            for i in result:
                link = i['href']
                links.append(f'https://kolesa.kz{link}')

            for i in links:
                if (i not in database):
                    print(i)
                    database.append(i)
                    database.reverse()
                    print(i) # В этой строке кода нужно будет отправлять сообщение (как в main.py)
                    with open(self.files[url], "w") as write_file:
                        json.dump(database, write_file)
                    write_file.close()



# DEBUG

# Как сделать запрос из телеграм бота: /add_car марка:бмв пробег:да максгод:2020
# Разделить строку через split

def debug_parse():
    import time
    a = Parser()
    b = a.make_query(marka='bmw', probeg='old', year_final=2020, )
    c = a.make_query(city='алматы', marka='vaz', probeg='old', year_final=2020, price_final=10000000)
    print(c)
    a.add_car(b)
    a.add_car(c)
    a.parse_cars()
    while True:
        time.sleep(10)
        a.parse_cars()

def debug_adding(arg:str):
    a = Parser()
    arg = arg.split()[1:]# Срез только на дебаге, т.к. в самом боте /add_car уберется
    # city=None, marka=None, probeg=None, kredit=None, type=1, year_start=None,
    # year_final=None, price_start=None, price_final=None

    city = None
    marka = None
    probeg = None
    kredit = None
    type = 1
    year_start = None
    year_final = None
    price_start = None
    price_final = None

    print(arg)

    for i in arg:
        i = i.split(':')
        if(i[0] == 'Город'):
            city = i[1]
        elif(i[0] == 'Марка'):
            marka = i[1]
        elif(i[0] == 'Пробег'):
            probeg = i[1]

    c = a.make_query(city=city, probeg=probeg, marka=marka)
    print(c)

az = input()

debug_adding(az)

