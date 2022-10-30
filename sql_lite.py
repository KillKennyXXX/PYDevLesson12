
# https://anflat.ru/rent/apartments/kazan/

# hh
# название, регион, ключевые скилы
# python developer, Москва, (python, sql)
# java delevoper, Питер, (java, spring)
# ruby, Москва, (python, ruby)

# Реляционная база
# Таблица, связи

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db.sqlite')

# Создаем курсор
cursor = conn.cursor()

cursor.execute('SELECT * from region')

result = cursor.fetchall()
print(result)

for item in result:
    print(item)
    print(type(item))

cursor.execute('SELECT * from region where name=?', ('Москва',))

print(cursor.fetchall())

# Если запрос ничего не возращает то делаем execute
cursor.execute("insert into vacancykey_skills (vacancy_id, key_skills_id) VALUES (?, ?)", (1, 5))

cursor.execute('SELECT * from vacancykey_skills')

print(cursor.fetchall())

query = 'select vk.id, v.name, k.name, r.name from vacancy v, ' \
        'key_skills k, vacancykey_skills vk, region r where vk.vacancy_id = v.id' \
        ' and vk.key_skills_id = k.id and v.region_id = r.id'

# Вывести в нормальном виде таблицу скилы + вакансии
cursor.execute(query)

print(cursor.fetchall())