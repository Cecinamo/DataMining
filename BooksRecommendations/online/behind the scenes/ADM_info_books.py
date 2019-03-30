# BOOKS
import pandas as pd
import re
import csv
# importiamo
f = open('BX-Books.csv', 'r')
Books = []
for row in f:
    row = re.sub('&amp;','&',row)
    row = row[:-2].split('";"')
    # modifichiamo ISBN come sopra
    row[0] = re.sub('[^A-Za-z0-9;]','',row[0]).upper()
    Books.append(row)
books = {}
for t in range(len(Books[0])):
    books[Books[0][t]] = [b[t] for b in Books[1:]]
Books = pd.DataFrame(data=books)

# YEAR OF PUBLICATION
yop = pd.Series(list(map(int,Books['Year-Of-Publication'])), index = Books.index)
print(yop)
n = 0
for i in yop.index:
    if yop[i]>2016 or yop[i]==0:
        yop[i] = 0
    elif yop[i]<1800:
        yop[i] = 1
    elif yop[i]<1900:
        yop[i] = 2
    else: 
        yop[i] = 3+int((yop[i]-1900)/10)
    if n<100:
        print(Books['Year-Of-Publication'][n],yop[i])
    n+=1

# BOOK-AUTHOR
# per quanto riguarda book-author buttiamo al cesso tutto cio' che non e' l'ultima parola che supponiamo sia il cognome.. anche se
# puo' essere che si come puo' essere che no. mettiamo pure lower visto che c'e' chi ha avuto la brillante idea di scrivere i nomi
# tutti maiuscoli.
ba = Books['Book-Author'].copy()
for i in ba.index:
    ba[i] = ba[i].split()[-1].lower()
    if i<100:
        print(Books['Book-Author'][i],ba[i])

# BOOK-TITLE	
# per quanto riguarda il titolo del libro facciamo un po' di pulizie......
import nltk
from nltk.corpus import stopwords
sw = stopwords.words('english')
bt = Books['Book-Title'].copy()
for i in bt.index:
    bt[i] = bt[i].lower()
    bt[i] = re.findall('[a-z0-9]+',bt[i])
    app = []
    for w in bt[i]:
        if w not in sw:
            app.append(nltk.PorterStemmer().stem_word(w))
    bt[i] = ' '.join(app)
    if i<100:
        print(Books['Book-Title'][i],'\n',bt[i])

# A questo punto proviamo a creare un nuovo DataFrame con tutte le informazioni
import json
info = {}
for b in Books.index:
    info[Books['ISBN'][b]] = {
        'book-title': bt[b],
        'book-author': ba[b],
        'year-of-publication': str(yop[b]),
        'publisher': Books['Publisher'][b]
    }

file = open('info_books.json','w')
json.dump(info,file)