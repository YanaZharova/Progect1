import csv

G = {}
node_colors =[]

Names = []
all_authors = set()
with open(" MATERIALS SCIENCE MULTIDISCIPLINARY 2016.csv") as r_file:
    file = csv.DictReader(r_file, delimiter = ";")
    for item in file:
        if item['статья'] != 'неважно':
            if item['авторы'] == '[]':
                authors = ['Nobody']
            else:
                authors = item['авторы'][1:-1].replace("'", "").replace('"', '').split(',')
            for i in range(len(authors)):
                if authors[i][0] == ' ':
                    #print(authors[i])
                    authors[i] = authors[i][1:]
                    #print(authors[i])
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
#print(list_authors)
for i in range(len(Names)):
    for j in range(len(Names[i]['cited'])):
        if Names[i]['cited'][j][0] == ' ':
            Names[i]['cited'][j] =  Names[i]['cited'][j][1:]       
        c = Names[i]['cited'][j].split()
        for k in list_authors:
            a = k.split()
            if a[0] == c[0] and a[1][0] == c[1][0]:
                Names[i]['cited'][j] = k

for item in Names:
    for j in authors:
        #print(j)
        j.lstrip(' ')
        if j not in G.keys():
            G[j] = []
    for j in authors:
        for k in cited:
            k.lstrip()
            G[j].append(k)    
                    
# Поиск в глубину - ПВГ (Depth First Search - DFS)
def dfs(v, p):
    if v in visited:  # Если вершина уже посещена, выходим
        return
    visited.add(v)  # Посетили вершину v
    for i in G[v]:  # Все смежные с v вершины
        if i in G.keys():
            for j in p:
                if j not in G[i]:
                    return
            if not i in visited:
                cartel.append(i)
                p.append(i)
                dfs(i, p)
                

import networkx as nx                
Cartels = nx.Graph()
cartels = []
for i in G.keys():
    visited = set()  # Посещена ли вершина?
    cartel = set()
    cartel.add(i)
    p = []
    p.append(i)
    dfs(i, p)
    if cartel not in cartels and len(cartel) > 1:
        print(cartel)
        cartels.append(cartel)
        cartell = list(cartel)
        for j in cartell:
            if cartell.index(j) == 0:
                if i not in Cartels.nodes:
                    Cartels.add_node(j)
            else:
                if i not in Cartels.nodes:
                    Cartels.add_node(j)
                for k in cartell:
                    for l in cartell:
                        if k != l:
                            Cartels.add_edge(k, l)
        

nx.draw(Cartels, node_size=1000, with_labels=True, font_weight='bold')
        