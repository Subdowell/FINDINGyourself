import codecs
import os, sys
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()


from scraping.models import Vacancy, City, Language, Error
from scraping.parser import *

parser = (
    (hh_ru, 'https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python&from=suggest_post'),
    (praca_by, 'https://praca.by/search/vacancies/?search%5Bcities%5D%5B%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%5D=1&search%5Bquery%5D=python&search%5Bdistance%5D%5B50000%5D=1&search%5Bhome-address%5D=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&search%5Bquery-text-params%5D%5Bheadline%5D=1&form-submit-btn=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8'),
    # (djinni_co, 'https://djinni.co/jobs/keyword-python/')
)
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []

for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.json', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
