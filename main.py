import requests
from fake_useragent import UserAgent

import os

ua = UserAgent().random

headers = {
    'User-Agent': ua,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}


def get_pages(*, per_page, pagen):
    res = requests.get(f'https://chaturanga.yoga/asanas/?PER_PAGE={per_page}&PAGEN_1={pagen}')
    src = res.text

    if not os.path.isdir('html_pages'):
        os.mkdir('html_pages')

    with open(f'html_pages/page_{pagen}.html', 'w', encoding='utf-8') as file:
        file.write(src)


if __name__ == '__main__':
    for pagen in range(1, 5):
        get_pages(per_page=100, pagen=pagen)