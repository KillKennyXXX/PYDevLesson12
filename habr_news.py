import re
from datetime import datetime
from csv import DictWriter

from bs4 import BeautifulSoup
from requests import get

url = f'https://habr.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

res = get(url + '/ru/news', headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
news = [tag['href'] for tag in soup.find_all('a', class_='tm-article-snippet__readmore') if 'company' not in tag['href']]
# print(news)


with open('base.csv', mode='w', encoding='utf8') as f:
    tt = DictWriter(f, fieldnames=['date', 'avtor', 'title', 'link', 'img', 'text'], delimiter=';')
    tt.writeheader()
    for new in news:
        row = {}
        res = get(url + new, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find_all('span', class_='')
        row['title'] = title[0].text
        row['link'] = url + new

        date = soup.find_all('time')
        date = date[0]
        row['date'] = date['title']

        avtor = soup.find_all('a', class_='tm-user-info__username')
        row['avtor'] = avtor[0].text.replace('\n', '').replace(' ', '')

        img = soup.find_all('img', class_='')
        img = img[0]
        row['img'] = img['src']
        text = ''
        for tag in soup.find_all('p', class_=''):
            text += tag.text
        row['text'] = text
        tt.writerow(row)
