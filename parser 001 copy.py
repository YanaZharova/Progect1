import requests
from bs4 import BeautifulSoup
import csv

#для теста использовался url https://apps.webofknowledge.com/Search.do?product=WOS&SID=5FdNab3RfRGoRy8tasV&search_mode=AdvancedSearch&prID=eb666338-0f43-46c7-a537-42e1964dfca5
#я точно не знаю, через сколько, но ссылка станет не рабояей
HEADERS = {'username': 'скрыто из соображений безопастности', 'password': 'скрыто из соображений безопастности', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
HOST = 'https://apps.webofknowledge.com'

def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('span', id='pageCount.top').get_text()
    pagination = int(pagination.replace(",", ""))
    print(pagination)
    return pagination

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='search-results-content')
    documents = []
    for item in items:
        documents.append(HOST + item.find('a', class_='smallV110 snowplow-full-record').get('href'))
    #print(documents)
    return documents

# можно ли хранить в облаке
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link'])
        for item in items:
            writer.writerow([item['title'], item['link']])
    
    


def parse():
    URL = input('Введите URL: ')
    html = get_html(URL)
    if html.status_code == 200:
        print('YES')
        documents = []
        pages_count = get_pages_count(html.text)
        print('Cтраница...', end='')
        for page in range(1, pages_count+1):
            print(str(page), end=', ')
            html = get_html(URL, params={'page': page})
            documents.extend(get_content(html.text))
        print(documents)
    else:
        print('ЕРОР 404!!11!!!')
    return documents
    


def get_names(html):
    soup = BeautifulSoup(html, 'html.parser')
    authors = soup.find_all('a', title='Найти еще записи для этого автора')
    #cited = soup.find_all('div', class_='search-results-content')
    qk = int(soup.find('div', class_='card-box').find_all('span', class_='large-number')[1].get_text())
    print(qk)
    if qk != 0:
        if qk > 30:
            Go = HOST + '/' + soup.find('a', class_='view-all-link snowplow-view-all-in-cited-references-page-bottom').get('href')
            html = get_html(Go)
            #soup1 = BeautifulSoup(html, 'html.parser')
            #cited = []
            #cited_have = soup1.find_all
        else:
            a = 0
    names = []
    authors_edit = []
    
    for author in authors:
        authors_edit.append(author.get_text().replace(',', ''))
        
    names.append({
        'authors': authors_edit
        #'cited': citated
    })
    #print(documents)
    return names

def parse_names(link_list):
    who_cited_who = []
    for link in link_list:
        html = get_html(link)
        if html.status_code == 200:
            print('YES')
            who_cited_who.extend(get_names(html.text))
        else:
            print('ЕРОР 404!!11!!!')
    return who_cited_who
            
documents = parse()
who_cited_who = parse_names(documents)

# сохранять в облако нецелесообразно
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['кто']) #будет еще и 'кого'
        for item in items:
            writer.writerow([*item['authors']])

file = 'citation1.csv'
save_file(who_cited_who, file)