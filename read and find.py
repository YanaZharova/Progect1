import csv
import networkx as nx

G = nx.Graph()
node_colors =[]

with open("citation test005.csv") as r_file:
    file = csv.reader(r_file, delimiter = ";")
    for item in file:
        if item['статья'] != 'неважно':
            authors = item['авторы'][1:-1].replace("'", "").split(',')
            cited = item['цитируют'][1:-1].replace("'", "").split(',')
            for j in authors:
                if j not in G.nodes:
                    G.add_node(j)
                    node_colors.append('r')
            for j in authors:
                for k in cited:
                    if k not in G.nodes:
                        G.add_node(k)
                        node_colors.append('b')
                    if (j, k) not in G.edges:
                        G.add_edge(j, k)  
                        
nx.draw(G, node_color = node_colors, node_size=1000, with_labels=True, font_weight='bold')