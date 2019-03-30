import json
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

# BOOKS ha doppioni
len(Books['ISBN'])-len(set(Books['ISBN']))  #315

INFO = {}
for row in range(Books.shape[0]):
    info = {}
    info['Book-Title'] = Books['Book-Title'][row]
    info['Book-Author'] = Books['Book-Author'][row]
    info['Year-Of-Publication'] = Books['Year-Of-Publication'][row]
    info['Publisher'] = Books['Publisher'][row]
    isbn = Books['ISBN'][row]
    INFO[isbn] = info
    print(info)

file = open('info_books(original).json','w')
json.dump(INFO,file)