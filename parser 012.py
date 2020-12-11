import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {'username': 'скрыто по соображениям безопастности', 'password': 'аналогично', 'User-Agent': 'аналогично', 'accept': '*/*'}
HOST = 'https://apps.webofknowledge.com'

def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_cited(url, many):
    html = get_html(url)
    if many % 30 == 0:
        pages_count = many // 2
    else:
        pages_count = many % 30 + 1    
    soup = BeautifulSoup(html.text, 'html.parser')
    cited = []
    for page in range(1, pages_count+1):
        htmla = get_html(url, params={'page': page})
        soupa = BeautifulSoup(htmla.text, 'html.parser')
        persons = soupa.find_all('a', title="Find more records by this author")
        cited.extend(persons)
    return cited

def get_names(html):
    soup = BeautifulSoup(html, 'html.parser')
    qk = int(soup.find('div', class_='card-box').find_all('span', class_='large-number')[1].get_text().replace(',', ''))
    print(qk)
    if qk != 0:      
        name_text = soup.find('div', class_='title').find('value').get_text()
        print(name_text)
        name_magazine = soup.find('div', class_='block-record-info block-record-info-source').find('span', class_='sourceTitle').find('value').get_text()
        authors = soup.find_all('a', title='Find more records by this author')
        authors_edit = []
        for author in authors:
            authors_edit.append(author.get_text().upper().replace(',', '').replace('.', ''))         
        Go = HOST + '/' + soup.find('a', class_='snowplow-citation-network-cited-reference-count-link').get('href')
        cited = get_cited(Go, qk)
        citated = []
        if cited == []:
            citated = ['Nobody']
        else:
            for i in cited:
                a = i.get_text().upper().replace(',', '').replace('.', '')
                if a not in citated and a not in authors_edit:
                    citated.append(a)
        with open('ENGINEERING ELECTRICAL ELECTRONIC 2018.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([name_text, authors_edit, citated, name_magazine, 'Russia'])

def parse(n_start, n_finish):
    URL = input('Введите URL: ')
    for doc in range(n_start, n_finish+1):
        if doc % 10 != 0:
            page = doc//10+1
            html = get_html(URL, params={'page': page, 'doc': doc})
            get_names(html.text)
        else:
            page = doc//10
            html = get_html(URL, params={'page': page, 'doc': doc})
            get_names(html.text)
            
with open('ENGINEERING ELECTRICAL ELECTRONIC 2018.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';') 
        writer.writerow(['статья', 'авторы', 'цитируют', 'журнал', 'страна'])
                   
n_start = int(input('с какой статьи начать '))        
n_finish = int(input('какой закончить '))
parse(n_start, n_finish)