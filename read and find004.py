import csv
import networkx as nx

G = nx.Graph()
node_colors =[]

Names = []
all_authors = set()
with open("PHYSICS MULTIDISCIPLINARY 2020.csv") as r_file:
    file = csv.DictReader(r_file, delimiter = ";")
    for item in file:
        if item['статья'] != 'неважно':
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
            if len(a) == 1 or len(c) == 1:
                continue             
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

go_authors = []
for item in Names2:
    for j in item['authors']:
        j.lstrip(' ')
        if j not in G.nodes:
            G.add_node(j)
            node_colors.append('r')
            go_authors.append(j)        
    for j in item['authors']:
        for k in item['cited']:
            k.lstrip()
            if k not in G.nodes:
                G.add_node(k)
                node_colors.append('b')
            if (j, k) not in G.edges:
                G.add_edge(j, k)  
            

cycles = []
all_len = []
for i in go_authors:
    try:
        cycle = nx.find_cycle(G, i, orientation="original")
        if cycle not in cycles:
            cycles.append(cycle)
            all_len.append(len(cycle))
    except:
        pass
    
CG = nx.Graph()
for i in cycles:
    for j in i:
        if j[0] not in CG.nodes:
            CG.add_node(j[0])
        if j[1] not in CG.nodes:
            CG.add_node(j[1])
        if (j[0], j[1]) not in CG.edges:
            CG.add_edge(j[0],j[1])
#nx.draw(G, node_color = node_colors, node_size=1000, with_labels=True, font_weight='bold')
print('колличество циклов: ', len(cycles))        
print('максимальная длинная цикла: ', max(all_len))
print('манимальная длинная цилка: ', min(all_len))
print('средняя длинная цикла: ', sum(all_len)/len(cycles))
print('количество участников циклов', len(CG.nodes))
print('всего авторов', len(G.nodes))

#nx.draw(CG, node_size=1000, with_labels=True, font_weight='bold')