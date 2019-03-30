# BOOK RATINGS
import pandas as pd
import json
BR = pd.read_csv('BR_cleaned.csv', sep='\t', encoding='utf8')
ratings = {}
for i in range(len(BR)):
    print(i)
    r = {}
    user = str(BR['User-ID'][i])
    book = str(BR['ISBN'][i].upper())
    rating = str(BR['Book-Rating'][i])
    r[user] = rating
    if book in ratings.keys():
        ratings[book].update(r)
    else:
        ratings[book] = r
print(ratings)
file = open('ratings_books(cleaned).json','w')
json.dump(ratings,file)