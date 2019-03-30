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
    r[book] = rating
    if user in ratings.keys():
        ratings[user].update(r)
    else:
        ratings[user] = r
print(ratings)
file = open('ratings_users(cleaned).json','w')
json.dump(ratings,file)