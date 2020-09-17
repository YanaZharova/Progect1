import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.elibrary.ru/projects/subscription/rus_titles_free.asp'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36', 'accept': '*/*'}
HOST = 'https://www.elibrary.ru'
FILE = 'magazines.csv'

def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

# в elibrary нет страниц
#def get_pages_count(html):
    #soup = BeautifulSoup(html, 'html.parser')
    #pageSS = soup.find_all('td', class_='mouse-hoverger')

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('table', id='restab').find_all('a')
    magaz = []
    for item in items:
        magaz.append({
            'title': item.get_text(),
            'link': HOST + item.get('href')
        })
    return magaz

# можно ли хранить в облаке
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'link'])
        for item in items:
            writer.writerow([item['title'], item['link']])
    
    
    
def parse():
    #URL = input('Введите URL: ')
    html = get_html(URL)
    if html.status_code == 200:
        magazine = []
        
        #pages_count = get_pages_count(html.text)
        magazines = get_content(html.text)
        #save_file(magazines, FILE) сохранение в облако
    else:
        print('ЕРОР 404!!11!!!')
    

parse()