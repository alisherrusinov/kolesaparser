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
        }
        self.links = []
        self.files = {}
        # https://kolesa.kz/cars/avtomobili-s-probegom/avtokredit/nissan/almaty/
        # ?auto-car-grbody=2&year[from]=2004&year[to]=2020&price[from]=1%20000&price[to]=100%20000%20000
        # https://kolesa.kz/cars/PROBEG/KREDIT/MARKA/CITY/

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
        print(f'{url[:10]}{len(self.links)}.txt')
        file = open(f'{len(self.links)}.txt', 'w')
        file.close()
        self.files[url] = f'{len(self.links)}.txt'

    def parse_cars(self):
        req = requests.get()
        if (req.status_code == 404):
            print('Неверная ссылка')
            return False
        parser = BeautifulSoup(req.text, 'lxml')

        list_links = parser.find_all('div', {'class': 'row vw-item list-item a-elem'})
        result = []
        for th in list_links:
            result.extend(th.find_all('span', {'class': 'a-el-info-title'}))
        result1 = []
        for th in result:
            result1.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id': 'main'}))
        for i in result1:
            print(i['href'])




a = Parser()
b = a.make_query(city='алматы', marka='vaz', probeg='old', year_final=2020, price_final=10000000)
a.add_car('http:azazazaza/')
a.add_car('http:aaaaaa/')
print(a.links)
print(a.files)
