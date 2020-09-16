import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('hh_ru', 'praca_by', 'djinni_co', 'belmeta')

headers = [
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           },
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           },
           {'User-Agent': 'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           }
          ]


def hh_ru(url, city=None, language=None):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0,2)])
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs= {'class': 'vacancy-serp'})
            if main_div:
                div_lst = main_div.find_all('div',attrs= {'class': 'vacancy-serp-item'})
                for div in div_lst:
                    title = div.find('span', attrs = {'class': 'g-user-content'})
                    href = title.a['href']
                    content = div.find('div', attrs = {'class': 'g-user-content'}).text
                    company = 'No name'
                    com = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info'}).a.text
                    if com:
                        company = com
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

def praca_by(url, city=None, language=None):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0,2)])
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'search-list'})
            if main_ul:
                ul_lst = main_ul.find_all('li', attrs={'class': 'vac-small'})
                for ul in ul_lst:
                    title = ul.find('div', attrs={'class': 'vac-small__title'})
                    href = title.a['href']
                    company = ul.find('div', attrs={'class': 'vac-small__upd'}).a.text
                    jobs.append({'title': title.text, 'url': href, 'company': company,
                                 'city_id': city, 'language_id': language})

            else:
                errors.append({'url': url, 'title': 'Ul does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

def rabota_ua(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers[randint(0,2)])
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class':'f-vacancylist-newnotfound'})
            if not new_jobs:
                main_tb = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if main_tb:
                    tr_lst = main_tb.find_all('tr', id=True)
                    for tar in tr_lst:
                        div = tar.find('div', attrs = {'class': 'card-body'})
                        if div:
                            title = div.find('p', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.find('div', attrs={'class': 'card-description'}).text
                            company = 'No name'
                            p = div.find('p', attrs= {'class': 'company-name'})
                            if p:
                                company = p.a.text
                            jobs.append({'title': title.text, 'url': domain + href,
                                         'descriptions': content, 'company': company,
                                         'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'Table does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page is empty'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

def djinni_co(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    resp = requests.get(url, headers=headers[randint(0,2)])
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class':'f-vacancylist-newnotfound'})
            if not new_jobs:
                main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
                if main_ul:
                    ul_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
                    for ul in ul_lst:
                        title = ul.find('div', attrs={'class': 'list-jobs__title'})
                        href = title.a['href']
                        content = ul.find('p').text
                        company = 'No name'
                        a = ul.find('div', attrs={'class': 'list-jobs__details__info'}).text
                        if a:
                            company = a
                        jobs.append({'title': title.text, 'url': domain + href,
                                    'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'Section does not exists'})
            else:
                errors.append({'url': url, 'title': 'Page is empty'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

def belmeta(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://belmeta.com'
    resp = requests.get(url, headers=headers[randint(0,2)])
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs= {'class': 'jobs'})
            if main_div:
                article_lst = main_div.find_all('article',attrs= {'class': 'job'})
                for article in article_lst:
                    title = article.find('h2', attrs = {'class': 'title'})
                    href = title.a['href']
                    content = article.find('div', attrs = {'class': 'desc'}).text
                    company = 'No name'
                    com = article.find('div', attrs = {'class': 'job-data company'}).text
                    if com:
                        company = com
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://belmeta.com/vacansii?q=Python&l=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA'
    jobs, errors = belmeta(url)
    h = codecs.open('work.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
