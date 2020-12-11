import csv

G = {}
node_colors =[]

Names = []
all_authors = set()
with open("PHYSICS_MULTIDISCIPLINARY_2018.csv") as r_file:
    file = csv.DictReader(r_file, delimiter = ";")
    for item in file:
        if item['стать€'] != 'неважно':
            if item['авторы'] == '[]':
                authors = ['Nobody']
            else:
                authors = item['авторы'][1:-1].replace("'", "").replace('"', '').split(',')
            for i in range(len(authors)):
                if authors[i][0] == ' ':
                    authors[i] = authors[i][1:]
                all_authors.add(authors[i])
            if item['цитируют'] =='[]' or item['цитируют'] == []:
                cited = ['Nobody']
            else:
                cited = item['цитируют'][1:-1].replace("'", "").replace('"', '').split(',')
            Names.append({
            'authors': authors,
            'cited': cited
            })
            
list_authors = list(all_authors)
for i in range(len(list_authors)):
    auth1 = list_authors[i].split()
    if len(auth1) == 1:
        continue
    list_authors[i] = auth1[0] + ' ' + auth1[1][0]
    for j in range(len(list_authors)):
        if i != j and list_authors[i]!=list_authors[j]:
            auth2 = list_authors[j].split()
            if len(auth1) == 1 or len(auth2)==1:
                continue            
            if auth1[0]==auth2[0] and auth1[1][0]==auth2[1][0]:
                list_authors[j] = auth1[0] + ' ' + auth1[1][0]

all_authors = set(list_authors)
list_authors = list(all_authors)
for i in range(len(Names)):
    for j in range(len(Names[i]['authors'])):      
        c = Names[i]['authors'][j].split()
        for k in list_authors:
            a = k.split()
            if len(a) == 1 or len(c) == 1:
                continue            
            if a[0] == c[0] and a[1][0] == c[1][0]:
                Names[i]['authors'][j] = k
                
for i in range(len(Names)):
    for j in range(len(Names[i]['cited'])):
        if Names[i]['cited'][j][0] == ' ':
            Names[i]['cited'][j] =  Names[i]['cited'][j][1:]       
        c = Names[i]['cited'][j].split()
        for k in list_authors:
            a = k.split()
            if a[0] == c[0] and a[1][0] == c[1][0]:
                Names[i]['cited'][j] = k

Names2 = []
for i in Names:
    au = set(i['authors'])
    ci = set(i['cited'])
    if not au.isdisjoint(ci):
        ci -= au
    Names2.append({
        'authors': list(au),
        'cited': list(ci)
        })
    
for item in Names2:
    for j in item['authors']:
        j.lstrip(' ')
        if j not in G.keys():
            G[j] = []
    for j in item['authors']:
        for k in item['cited']:
            k.lstrip()
            G[j].append(k)    
                    
# ѕоиск в глубину - ѕ¬√ (Depth First Search - DFS)
def dfs(v, p):
    if v in visited:  # ≈сли вершина уже посещена, выходим
        return
    visited.add(v)  # ѕосетили вершину v
    for i in G[v]:  # ¬се смежные с v вершины
        if i in G.keys():
            for j in p:
                if j not in G[i]:
                    return
            if not i in visited:
                cartel.add(i)
                for k in p:
                    cartel_edge.append((i, k))
                p.append(i)
                dfs(i, p)
                

import networkx as nx                
Cartels = nx.Graph()
cartels = []
cartel_len = []
for i in G.keys():
    visited = set()  # ѕосещена ли вершина?
    cartel = set()
    cartel.add(i)
    p = []
    p.append(i)
    cartel_edge = []
    dfs(i, p)
    if cartel not in cartels and len(cartel) > 1:
        cartel_len.append(len(cartel))
        cartels.append(cartel)
        cartell = list(cartel)
        for j in cartell:
            if j not in Cartels.nodes:
                Cartels.add_node(j)
        Cartels.add_edges_from(cartel_edge)



print('2 mafia')
for i in cartels:
    if len(i) == 2:
        print(i)
        
print('3 mafia')
for i in cartels:
    if len(i) == 3:
        print(i)        

print('4 mafia')
for i in cartels:
    if len(i) == 4:
        print(i)

print('more mafia')
for i in cartels:
    if len(i) > 4:
        print(i)
        
print('колличество картелей: ', len(cartels))        
print('максимальна€ длинна€ картел€: ', max(cartel_len))
print('манимальна€ длинна€ картел€: ', min(cartel_len))
print('средн€€ длинна€ картел€: ', sum(cartel_len)/len(cartels))
print('участников картелей', len(Cartels.nodes))
nx.draw(Cartels, node_size=1000, with_labels=True, font_weight='bold')