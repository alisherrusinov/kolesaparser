import requests
from bs4 import BeautifulSoup

req = requests.get('https://kolesa.kz/cars/avtomobili-s-probegom/vaz/')
print(req)
parser = BeautifulSoup(req.text, 'lxml')

list_links = parser.find_all('div', {'class': 'row vw-item list-item a-elem'})
result = []
for th in list_links:
    result.extend(th.find_all('span', {'class': 'a-el-info-title'}))
result1 = []
for th in result:
    result1.extend(th.find_all('a', {'class': 'list-link ddl_product_link', 'data-list-id':'main'}))
for i in result1:
    print(i['href'])
