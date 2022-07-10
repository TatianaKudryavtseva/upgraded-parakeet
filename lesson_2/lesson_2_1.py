import requests
from bs4 import BeautifulSoup
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/103.0.0.0 Safari/537.36'}
url = 'https://hh.ru'
vacancy_search = 'analitik'
params = {'page': '0',
          'hhtmFrom': 'vacancy_search_catalog'}
session = requests.Session()
response = session.get(url + '/vacancies/' + vacancy_search,
                       headers=headers, params=params)

dom = BeautifulSoup(response.text, 'html.parser')
vacancies = dom.find_all('div',
                         {'class': 'vacancy-serp-item-body__main-info'})
last_page = dom.find('a', {'data-qa': 'pager-next'}).previous_sibling
last_page = last_page.find('a', {'data-qa': 'pager-page'}).text
vacancies_list = []

for i in range(int(last_page)):
    print(f'scrapping page {i}')
    params['page'] = i
    response = session.get(url + '/vacancies/' + vacancy_search,
                           headers=headers, params=params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div',
                             {'class': 'vacancy-serp-item-body__main-info'})
    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        href = name.get('href')
        name = name.text
        salary = vacancy.find('span',
                              {'data-qa': 'vacancy-serp__vacancy-compensation'}
                              )
        salary_min = 'none'
        salary_max = 'none'
        salary_currency = ''
        if salary:
            salary = salary.text.replace('\u202f', '').split(' ')
            if salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = 'none'
                salary_currency = str(salary[2])
            elif salary[0] == 'до':
                salary_min = 'none'
                salary_max = int(salary[1])
                salary_currency = str(salary[2])
            elif len(salary) == 4:
                salary_min = int(salary[0])
                salary_max = int(salary[2])
                salary_currency = str(salary[3])

            vacancy_data['site'] = url
            vacancy_data['name'] = name
            vacancy_data['href'] = href
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency

            vacancies_list.append(vacancy_data)

with open(f"{vacancy_search}.json", "w") as write_file:
    json.dump(vacancies_list, write_file, ensure_ascii=False)
