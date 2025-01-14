from bs4 import BeautifulSoup

import os
import csv

main_url = 'https://chaturanga.yoga'


def get_urls(page_num):
    with open(f'html_pages/page_{page_num}.html', 'r') as file:
        page = file.read()

    soup = BeautifulSoup(page, 'lxml')

    catalog = soup.find(class_='catalog__wrap')
    links = catalog.find_all('a', href=True)

    urls = []
    for link in links:
        href = link.get('href')
        urls.append(main_url + href)

    if not os.path.isdir('data'):
        os.mkdir('data')

    with open('data/asanas_urls.csv', 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for url in urls:
            writer.writerow([url])


if __name__ == '__main__':
    for page_num in range(1, 5):
        get_urls(page_num)