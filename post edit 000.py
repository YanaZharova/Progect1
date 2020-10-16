import csv
import os
G = {}
Names = []
all_authors = set()
with open(" MATERIALS SCIENCE MULTIDISCIPLINARY 2016.csv") as r_file:
    file = csv.DictReader(r_file, delimiter = ";")
    for item in file:
        if item['статья'] != 'неважно':
            if item['авторы'] == '[]':
                authors = ['Nobody']
            else:
                authors = item['авторы'][1:-1].replace("'", "").split(',')
            for i in range(len(authors)):
                if authors[i][0] == ' ':
                    #print(authors[i])
                    authors[i] = authors[i][1:]
                    #print(authors[i])
                all_authors.add(authors[i])
            if item['цитируют'] =='[]' or item['цитируют'] == []:
                cited = ['Nobody']
            else:
                cited = item['цитируют'][1:-1].replace("'", "").split(',')
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
            #print(k)
            a = k.split()
            #print(a)
            #print(c)
            #print(j)
            if a[0] == c[0] and a[1][0] == c[1][0]:
                Names[i]['cited'][j] = k
            
                
for i in Names:
    print(i)