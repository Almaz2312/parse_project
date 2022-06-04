import requests
from bs4 import BeautifulSoup
import csv
URL = f"https://cars.kg/offers/?vendor=57fa24ee2860c45a2a2c093b"
HEADERS = {
    'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;'
                  ' rv:97.0) Gecko/20100101 Firefox/97.0',
    'accept': '*/*',
}


DOMEN = 'https://cars.kg'
toyota = []


def get_html(url, params=None):
    request_ = requests.get(url=url,
                           headers=HEADERS,
                           params=params)
    return request_


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', class_='main catalog')
    cars = soup.find_all('a', class_='catalog-list-item')
    for car in cars:
        try:
            img = car.find('img').get('src')
        except:
            img = 'no photo'

        toyota.append(
            {
                "title": car.find('span',
                                  class_='catalog-item-caption').get_text(strip=True),
                "description": car.find('span',
                                        class_='catalog-item-descr').get_text(strip=True),
                "image": img,
                "price_usd": car.find('span',
                                      class_='catalog-item-price').get_text(strip=True),
                "price_som": car.find('span',
                                      class_='catalog-item-price')['title'].replace('или ~', ''),
                "year": car.find('span',
                                 class_='caption-year').get_text(strip=True),

            }
        )

    return toyota


def download_csv(toyotas):
    with open('Toyotas.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Фото', 'Название', 'Описание', 'Год', 'Цена USD', 'Цена KGS'])
        for toyota_car in toyotas:
            writer.writerow([toyota_car['image'], toyota_car['title'],
                             toyota_car['description'], toyota_car['year'],
                             toyota_car['price_usd'], toyota_car['price_som']
                            ])
        print(len(toyotas))
        print('test')


def parse_cars():
    for i in range(1, 5):
        URL = f"https://cars.kg/offers/{i}?vendor=57fa24ee2860c45a2a2c093b"
        html_ = get_html(URL)
        print('status: ', html_.status_code)
        if html_.status_code == 200:
            toyotas = get_content(html_.text)
            download_csv(toyotas)
        else:
            print('connect error')


parse_cars()