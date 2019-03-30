import json
import numpy as np
import warnings
warnings.filterwarnings('ignore', '.*invalid value encountered-*',)
with open('ratings_books.json') as data_file:    
    ratings_books = json.load(data_file)
mbooks = {}
n = 0
for book in ratings_books.keys():
    print(n)
    vals = list(map(int,ratings_books[book].values()))
    vals = [v for v in vals if v!=0]
    m = np.mean(vals)
    print(ratings_books[book])
    if np.isnan(m): m=6
    print(m)
    mbooks[book] = float(m)
    n+=1
mb = {}
mb['books'] = mbooks
file = open('mbooks.json','w')
json.dump(mb,file)