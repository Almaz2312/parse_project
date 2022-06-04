import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                  'rv:97.0) Gecko/20100101 Firefox/97.0',
    'accept': '*/*',
}
URL = 'https://www.kivano.kg/bytovaya-tekhnika'

DOMEN = 'https://www.kivano.kg'


def get_html(url, params=None):
    request_ = requests.get(url=url,
                            headers=HEADERS,
                            params=params)
    return request_


def get_content_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="item product_listbox oh")
    washing_machine = []
    print(items)
    for item in items:
        washing_machine.append(
            {
                "title": item.find('div',
                                   class_='listbox_title oh').get_text().replace('\n', ''),
                "description": item.find('div',
                                         class_='product_text pull-left').get_text(),
                "image": DOMEN + item.find('img').get('src'),
                "price": item.find('div',
                                   class_='listbox_price text-center').get_text().replace('\n', '')
            }
        )
    return washing_machine


def download_csv(machines):
    with open('wash_machine.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Название', 'Описание', 'Картинка', 'Цена'])
        for machine in machines:
            writer.writerow([machine['title'], machine['description'],
                             machine['image'], machine['price']]
                            )


def parse_kivano():
    html_ = get_html(URL)
    if html_.status_code == 200:
        machines = get_content_page(html_.text)
        download_csv(machines)
    else:
        print('connect error!!!')


parse_kivano()


# ДЗ нужно убрать сомы и сконвертировать их в доллары

"""
ДЗ Спарсить cars.kg/ title/description/ photo/ price/ year/ 
"""