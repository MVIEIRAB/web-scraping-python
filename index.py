import requests
import csv
from bs4 import BeautifulSoup
import asyncio

pesquisa = input('Insira o nome do produto: ').replace(' ', '+')
baseurl = "https://www.amazon.com.br/s?k={}".format(pesquisa)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}

products_list = []
values_list = []


async def generateCSV():
    await getData()
    f = open("amazon_products_python.csv", "w")
    w = csv.writer(f)
    w.writerow(('NOME', 'PRECO'))
    try:
        for item in range(len(products_list)-1):
            w.writerow((products_list[item], values_list[item]))
    finally:
        f.close()
    if len(products_list) == 0:
        print('Nao conseguimos buscar este item, por favor tente novamente ou insira outro')
    else:
        print('Arquivo gerado com sucesso')


async def getData():
    print('Iniciando Consulta....')
    page = requests.get(baseurl, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    productsSection = soup.find_all(
        'div', {'data-component-type': 's-search-result'})
    await asyncio.sleep(2)

    option = 0

    for divs in productsSection:
        sections = divs.find(
            class_='sg-col-inner').find(class_='a-section').find_all(class_='a-spacing-top-small')

        for section in sections:
            produto = section.find_all(
                class_=["a-size-base-plus", "a-offscreen"])

            for prod in produto:
                string = prod.get_text().strip()

                if option == 0 and string.find('R$') == -1:
                    products_list.append(string)
                    option = 1
                    continue

                if option == 1 and string.find('R$') == 0:
                    values_list.append(string)
                    option = 0
                    continue

                if option == 1 and string.find('R$') == -1:
                    values_list.append('sem estoque')
                    option = 0
                    continue

loop = asyncio.get_event_loop()
loop.run_until_complete(generateCSV())
loop.close()
