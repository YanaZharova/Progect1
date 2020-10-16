import csv

G = {}
node_colors =[]

with open(" MATERIALS SCIENCE MULTIDISCIPLINARY 2016.csv") as r_file:
    file = csv.DictReader(r_file, delimiter = ";")
    for item in file:
        if item['статья'] != 'неважно':
            authors = item['авторы'][1:-1].replace("'", "").split(',')
            cited = item['цитируют'][1:-1].replace("'", "").split(',')
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
            if not i in visited and p in G[i]:
                cartel.append(i)
                dfs(i, p)            

import networkx as nx                
Cartels = nx.Graph()
cartels = []
for i in G.keys():
    visited = set()  # Посещена ли вершина?
    cartel = []
    cartel.append(i)
    p = i
    dfs(i, p)
    if cartel not in cartels and len(cartel) > 1:
        print(cartel)
        cartels.append(cartel)
        for j in cartel:
            if cartel.index(j) == 0:
                if i not in Cartels.nodes:
                    Cartels.add_node(j)
            else:
                if i not in Cartels.nodes:
                    Cartels.add_node(j)
                Cartels.add_edge(cartel[0], j)
        

nx.draw(Cartels, node_size=1000, with_labels=True, font_weight='bold')
        