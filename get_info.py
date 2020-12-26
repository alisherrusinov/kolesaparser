import requests
from bs4 import BeautifulSoup

req = requests.get('https://kolesa.kz/cars/avtomobili-s-probegom/vaz/')
print(req)
parser = BeautifulSoup(req.text, 'lxml')


# result1 = []
# for th in result:
#     result1.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id':'main'}))
# for i in result1:
#     print(i['href'])

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
driver.get('https://kolesa.kz/cars/avtomobili-s-probegom/vaz/')

html = driver.page_source
parser = BeautifulSoup(html, 'lxml')
list_blocks = parser.find_all('div', {'class': 'row vw-item list-item blue a-elem'})
spans = []  # Список штучек с заголовком объявления
for th in list_blocks:
    spans.extend(
        th.find_all('span', {'class': 'nb-views-int'}))  # Получение штучек с заголовком объявления
print(spans[0])
