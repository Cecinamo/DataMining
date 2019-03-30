# BOOK RATINGS
import pandas as pd
import re
import csv
import json
with open('books(ISBN).json') as data_file:    
    isbnbooks = json.load(data_file)
# importiamo i ratings
f = open('BX-Book-Ratings.csv', 'r')
BR = []
i = 0
for row in f:
    # tanto sono solo numeri a parte ISBN
    # quindi tutta la pulizia riguarda l'ISBN
    #row = re.sub('O','0',row.upper())
    i+=1
    #if i<100:
        #print(row)
    # la pulizia parte da i=2 in poi (i=1 e' il nome delle variabili!)
    if i!=1:
        # 3 o diventano 3 zeri
        row = re.sub('O{3}','000',row.upper())
        # 2 o diventano 2 zeri
        row = re.sub('O{2}','00',row)
        # cominciano per o diventano zero
        row = re.sub('(?<=["])O','0',row)
        # solo lettere diventa null
        row = re.sub('(?<=")[^0-9;]+(?=")','NULL',row)
        # piu' di tre lettere di seguito muore
        row = re.sub('[^0-9;]{3,}','',row)
        # tutto cio' che non e' lettera o numero o punto e virgola (che ci serve per lo split) muore
        row = re.sub('[^A-Za-z0-9;]','',row).upper()
    # eliminiamo le virgolette
    row = re.sub('["\n]','',row)
    # e splittiamo per il punto e virgola
    row = row.split(';')
    #if i<100:
        #print(row)
    # cosi' butto via pure le righe NULL (un ISBN valido e' lungo 10)
    if len(row[1])==10 or i==1:
        #print(row)
        BR.append(row)
# BR era una lista di liste.. a noi serve un dizionario che abbia una chiave per ogni variabile
br = {}
for t in range(len(BR[0])):
    # BR[0][t] e' la chiave (il nome) della variabile t-esima
    # b[t] sono i valori della variabile t-esima e partono da 1 in poi 
    # (sempre perche' BR[0] contiene i nomi)
    br[BR[0][t]] = [b[t] for b in BR[1:]]
BR = pd.DataFrame(data=br)

# creiamo nuovo file

u = []
b = []
r = []

for i in range(len(BR)):
    print(i)
    user = BR['User-ID'][i]
    book = BR['ISBN'][i].upper()
    rating = BR['Book-Rating'][i]
    if book in isbnbooks['ISBN']:
        u.append(user)
        b.append(book)
        r.append(rating)
d = {}
d['User-ID'] = u
d['ISBN'] = b
d['Book-Rating'] = r
BR_new = pd.DataFrame(data=d)
print(BR_new.head())
BR_new.to_csv('BR_cleaned.csv', index = False, sep='\t', encoding='utf8')