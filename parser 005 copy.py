import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {'username': 'скрыто', 'password': 'скрыто', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
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
        #documents = get_content(html.text)
        #save_file(magazines, FILE) сохранение в облако
        print(documents)
    else:
        print('ЕРОР 404!!11!!!')
    return documents

    
def get_cited(url):
    html = get_html(url)
    pages_count = get_pages_count(html.text)
    soup = BeautifulSoup(html.text, 'html.parser')
    cited = []
    for page in range(1, pages_count+1):
        htmla = get_html(url, params={'page': page})
        soupa = BeautifulSoup(htmla.text, 'html.parser')
        persons = soupa.find_all('a', title="Find more records by this author")
        cited.extend(persons)
    citated = []
    for i in cited:
        a = i.get_text().upper().replace(',', '').replace('.', '')
        if a not in citated:
            citated.append(a)
    return citated
    
    
    

def get_names(html):
    soup = BeautifulSoup(html, 'html.parser')
    name_text = soup.find('div', class_='title').find('value').get_text()
    print(name_text)
    name_magazine = soup.find('div', class_='block-record-info block-record-info-source').find('span', class_='sourceTitle').find('value').get_text()
    print(name_magazine)
    #country = soup.find('address').find('span', class_="hitHilite").get_text()
    #print(country)
    authors = soup.find_all('a', title='Find more records by this author')
    
    qk = int(soup.find('div', class_='card-box').find_all('span', class_='large-number')[1].get_text())
    print(qk)
    citated = []  
    if qk != 0:
        Go = HOST + '/' + soup.find('a', class_='snowplow-citation-network-cited-reference-count-link').get('href')
        citated = get_cited(Go)
        if citated == []:
            citated = ['Nobody']
    else:
        citated = ['Nobody']
    
    names = []
    authors_edit = []
    
    for author in authors:
        authors_edit.append(author.get_text().upper().replace(',', '').replace('.', ''))
        
      
    names.append({
        'name text': name_text,
        'authors': authors_edit,
        'cited': citated,
        'magazine': name_magazine,
        'country': 'Russia' #country проблеммы с СССР
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

# можно ли хранить в облаке
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['статья','авторы', 'цитируют', 'журнал', 'страна']) #будет еще и 'кого'
        for item in items:
            writer.writerow([item['name text'], item['authors'], item['cited'], item['magazine'], item['country']])

file = 'citation test004.csv'
#save_file(who_cited_who, file)

import networkx as nx
G = nx.Graph()

node_colors =[]

for item in who_cited_who:
    for j in item['authors']:
        if j not in G.nodes:
            G.add_node(j)
            node_colors.append('r')
    for j in item['authors']:
        for k in item['cited']:
            if k not in G.nodes:
                G.add_node(k)
                node_colors.append('b')
            if (j, k) not in G.edges:
                G.add_edge(j, k)
                

nx.draw(G, node_color = node_colors, node_size=1000, with_labels=True, font_weight='bold')

