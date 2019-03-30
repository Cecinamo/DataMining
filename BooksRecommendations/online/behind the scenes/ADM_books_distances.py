import json
import numpy as np
with open('info_books.json') as data_file:
    info_books = json.load(data_file)
keys = sorted(list(info_books.keys()))
J = {}
n = 0
for b1 in keys:
    print(n)
    #print(info_books[b1])
    j = {}
    b = []
    d = []
    for b2 in keys:
        if b2!=b1:
            #print(info_books[b2])
            v = 0 # intersezione
            if info_books[b2]['book-author']==info_books[b1]['book-author']:
                v+=0.3
            if (info_books[b1]['year-of-publication']!='0' and
                info_books[b2]['year-of-publication']==info_books[b1]['year-of-publication']):
                v+=0.2
            if info_books[b2]['publisher']==info_books[b1]['publisher']:
                v+=0.1
            titlew = info_books[b2]['book-title'].split() # parole del titolo
            t=0
            for w in titlew:
                if w in info_books[b1]['book-title']:
                    t+=1
                    if t == 2:
                        break
            v+=t*0.2
            #print(titlew)
            if v!=0:
                b.append(b2)
                d.append(v)
                #j[b2] = str(i/u)
                #print(j[b2])
    idxs = np.argsort(np.array(d))[-10:] #ce ne teniamo solo 10
    for i in idxs: j[b[i]]=str(d[i])
    J[b1] = j
    n+=1
file = open('books_distances.json','w')
json.dump(J,file)