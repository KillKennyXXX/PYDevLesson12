# Поиск вакансий
import time
import requests
import pprint
import json

proxies = {
    'http': 'http://167.86.96.4:3128',
    'https': 'http://167.86.96.4:3128',
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

# result = requests.get(url, headers=headers, proxies=proxies)



def save_stat(req, file_name):
    with open(file_name, 'w') as f:
        json.dump(req, f)


def getPages(search, area, page):
    params = {
        'text': 'NAME:(' + search + ')',
        'area': area,  # Поиск в зоне
        'page': page,  # Номер страницы
        'per_page': 100  # Кол-во вакансий на 1 странице
    }
    req = requests.get('https://api.hh.ru/vacancies', params=params)
    data = req.json()
    req.close()
    return data


def getKeysByUrls(urls):
    skills = []
    params = {'per_page': 100}
    count = 0
    countAll = len(urls)
    percent = 0

    for url in urls:
        # time.sleep(2)
        req = requests.get(url, params=params)
        data = req.json()
        for skill in data['key_skills']:
            if skill:
                skills.append(skill['name'])
        percent2 = int(count / countAll * 100)
        if percent != percent2:
            if percent == 50:
                print()
            print(percent2, end="% ")

        percent =percent2
        count += 1
    print()
    return skills


def getUrls(search):
    urls = []
    for page in range(0, 20):
        # time.sleep(2)
        jsObj = getPages(search, '1', page)
        if (jsObj['pages'] - page) >= 1:
            for obj in jsObj['items']:
                if obj['url']:
                    urls.append(obj['url'])
        else:
            break

    return urls

def getStatSkills(skills):
    key_skills = {}
    for skill in skills:
        if skill in key_skills:
            key_skills[skill] += 1
        else:
            key_skills[skill] = 1
    return key_skills

# for obj in getUrls():
#     if obj:
#         print(obj)
print('Формируем ссылки')
urls = getUrls('python')
print(urls)
print('Формируем скилы')
skills = getKeysByUrls(urls)
print(skills)
print('Формируем сводную таблицу по скилам')
key_skills = getStatSkills(skills)
result = sorted(key_skills.items(), key=lambda k: k[1], reverse=True)
print(result)
print('Сохраняем результаты')
save_stat(result, 'stat.json')




