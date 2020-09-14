import requests
import codecs
from bs4 import BeautifulSoup as BS


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
           }


def hh_ru(url):
    jobs = []
    errors = []
    url = 'https://hh.ru/search/vacancy?clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=Python'
    resp = requests.get(url, headers=headers)

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
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': href,
                             'descriptions': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def praca_by(url):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'search-list'})
        if main_ul:
            ul_lst = main_ul.find_all('li', attrs={'class': 'vac-small'})
            for ul in ul_lst:
                title = ul.find('div', attrs={'class': 'vac-small__title'})
                href = title.a['href']
                company = ul.find('div', attrs={'class': 'vac-small__upd'}).a.text
                jobs.append({'title': title.text, 'url': href, 'company': company})

        else:
            errors.append({'url': url, 'title': 'Ul does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

def rabota_ua(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    resp = requests.get(url, headers=headers)

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
                                     'descriptions': content, 'company': company})
            else:
                errors.append({'url': url, 'title': 'Table does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page is empty'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors

if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
    jobs, errors = rabota_ua(url)
    h = codecs.open('work.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
