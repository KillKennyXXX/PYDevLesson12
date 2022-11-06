from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()

# vacancyskill = Table('vacancyskill', Base.metadata,
#                      Column('id', Integer, primary_key=True),
#                      Column('vacancy_id', Integer, ForeignKey('vacancy.id')),
#                      Column('skill_id', Integer, ForeignKey('skill.id'))
#                      )


class Hh_region(Base):
    __tablename__ = 'hh_region'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    number = Column(Integer, nullable=True)

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'{self.id}) {self.name}: {self.number}'

class Hh_skills(Base):
    __tablename__ = 'hh_skills'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Hh_key(Base):
    __tablename__ = 'hh_key'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class About(Base):
    __tablename__ = 'about'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    subject = Column(String)
    message = Column(String)


    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message


    def __str__(self):
        return f'{self.id}) name: {self.name}, email: {self.email}, subject: {self.subject}, message: {self.message}'



class Hh_region_key_skills(Base):
    __tablename__ = 'hh_region_key_skills'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    num = Column(Integer, nullable=True)
    # Связь 1 - много, связь внешний ключ
    region_id = Column(Integer, ForeignKey('hh_region.id'))
    key_id = Column(Integer, ForeignKey('hh_key.id'))
    skills_id = Column(Integer, ForeignKey('hh_skills.id'))

    def __init__(self, name, num, region_id, key_id, skills_id):
        self.name = name
        self.num = num
        self.region_id = region_id
        self.skills_id = skills_id
        self.key_id = key_id


class Hh_urls(Base):
    __tablename__ = 'hh_urls'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # Связь 1 - много, связь внешний ключ
    region_id = Column(Integer, ForeignKey('hh_region.id'))
    key_id = Column(Integer, ForeignKey('hh_key.id'))


    def __init__(self, name, region_id, key_id):
        self.name = name
        self.region_id = region_id
        self.key_id = key_id
# Создание таблицы
Base.metadata.create_all(engine)

def save_about(name, email, subject, message):
    global engine
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(About(name, email, subject, message))
    session.commit()
    session.close()

def save_to_db(data, skills):
    global engine
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()
    # Регионы
    region = session.query(Hh_region).filter(Hh_region.number == data['area']).first()
    key = session.query(Hh_key).filter(Hh_key.name == data['key']).first()
    if not region:
        session.add_all([Hh_region('Москва', 1), Hh_region('Питер', 2)])
    session.flush()
    if not key:
        session.add(Hh_key(data['key']))
    session.flush()

    for key_s in skills.keys():
        skill = session.query(Hh_skills).filter(Hh_skills.name == key_s).first()
        if not skill:
            session.add(Hh_skills(key_s))

    session.flush()

    region = session.query(Hh_region).filter(Hh_region.number == data['area']).first()
    key = session.query(Hh_key).filter(Hh_key.name == data['key']).first()

    for url in data['urls']:
        url_table = session.query(Hh_urls).filter(Hh_urls.name == url).first()
        if not url_table:
            session.add(Hh_urls(url, data['area'], key.id))
    session.flush()


    for key_s, num_s in skills.items():
        skill = session.query(Hh_skills).filter(Hh_skills.name == key_s).first()
        session.add(Hh_region_key_skills(key_s, num_s, region.id, key.id, skill.id))
    session.commit()

    session.close()
def read_keys():
    global engine
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()
    keys = session.query(Hh_key).all()
    result = []
    for key in keys:
        result.append(key.name)
    return result

def read_top_skills_in_db(key, region):
    global engine
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()
    hh_region = session.query(Hh_region).filter(Hh_region.number == region).first()
    hh_key = session.query(Hh_key).filter(Hh_key.name == key).first()
    print(hh_region.id)
    print(hh_key.id)
    if key and region:
        skills = session.query(Hh_region_key_skills)\
            .filter(Hh_region_key_skills.key_id == hh_key.id) \
            .filter(Hh_region_key_skills.region_id == hh_region.id)\
            .order_by(Hh_region_key_skills.num.desc()).all()
        result = []
        for skill in skills[:15]:
            result.append((skill.name, skill.num))
        return result
    else:
        return 0

#
# # Выборка данных в регионе Москва
# # 1. id региона москва
# moscow = session.query(Region).filter(Region.name == 'Москва').first()
# print(moscow)
#
# # 2. вакансии в регионе москва
# vacancies = session.query(Vacancy).filter(Vacancy.region_id == moscow.id).all()
#
# print(len(vacancies))
# print(vacancies[0].region_id)

# print(read_top_skills_in_db('java', '1'))