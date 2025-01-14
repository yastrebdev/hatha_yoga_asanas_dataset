import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import os
import csv
import json

ua = UserAgent().random

main_url = 'https://chaturanga.yoga'

headers = {
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}


def get_data():
    asanas = []

    with open('data/asanas_urls.csv', 'r', encoding='utf-8') as csv_file:
        reader = list(csv.reader(csv_file))
        length = len(reader)

        for i, row in enumerate(reader):
            url = row[0]

            if not url.startswith('http'):
                print(f"Некорректный URL: {url}")
                continue

            res = requests.get(url=url, headers=headers)
            if res.status_code != 200:
                print(f"Ошибка запроса #{i}: {res.status_code} для URL {url}")
                continue

            src = res.text

            soup = BeautifulSoup(src, 'lxml')

            main_img_container = soup.find(class_='asana__slider__item')

            if main_img_container:
                main_img_src = main_img_container.find('img').get('src')
                main_img_url = main_url + main_img_src
            else:
                main_img_url = ''

            info_container = soup.find(class_='asana__container')
            asana_gold = info_container.find(class_='asana__gold')

            if asana_gold:
                asana_gold = True
            else:
                asana_gold = False

            title = info_container.find('h1')
            if title:
                title = title.text.strip()
            else:
                title = ''

            subtitle = info_container.find(class_='asana__content__subtitle').text.strip()

            if subtitle:
                en_title = subtitle.split('\n')[0].strip()
                translate_title = subtitle.split('\n')[-1].strip()
            else:
                en_title = ''
                translate_title = ''

            asana_pic_container = info_container.find(class_='asana__pics')

            asana_pic_url = ''
            if asana_pic_container:
                asana_pic_href = asana_pic_container.find('img').get('src')
                asana_pic_url = main_url + asana_pic_href

            description = info_container.find(class_='content')
            if description:
                description = description.text.strip()
            else:
                description = ''

            warning_container = info_container.find(class_='asana__warninng')
            if warning_container:
                warning = warning_container.find(class_='asana__warninng__text').text.strip()
            else:
                warning = ''

            asana_variants_container = soup.find(class_='asana__variants')

            if asana_variants_container:
                asana_variants_images = [
                    main_url + img.get('src') for img in asana_variants_container.find_all('img')
                ]
            else:
                asana_variants_images = []

            benefit_container = soup.find(class_='content-item gutter-top')

            if benefit_container:
                benefit = benefit_container.find(class_='content').text.strip().split('\n')[-1]
            else:
                benefit = ''

            asanas.append({
                'title': {
                    'ru': title,
                    'en': en_title,
                    'translate': translate_title
                },
                'gold_status': asana_gold,
                'preview': main_img_url,
                'pic': asana_pic_url,
                'description': description,
                'warning': warning,
                'asana_variants_images': asana_variants_images,
                'benefit': benefit
            })

            print(f'# Итерация {i + 1}/{length}')

    if not os.path.isdir('data'):
        os.mkdir('data')

    try:
        with open('data/asana_variants.json', 'w', encoding='utf-8') as json_file:
            json.dump(asanas, json_file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Ошибка записи JSON файлов: {e}")


if __name__ == "__main__":
    get_data()