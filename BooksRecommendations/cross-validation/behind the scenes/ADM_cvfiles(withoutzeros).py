# prendiamo tutto tranne i libri votati che non abbiamo in info_books
import json
import pandas as pd
import random
with open('ratings_users.json') as data_file:    
    ratings_users = json.load(data_file)
with open('info_books.json') as data_file:    
    info_books = json.load(data_file)

# users
users = list(ratings_users.keys())

# prendiamo tutti i libri letti da questi utenti
books = []
for u in users:
    for b in ratings_users[u].keys():
        books.append(b)

# eliminiamo libri che non esistono
print('nrows:',len(books))
nonexistingbooks = set(books).difference(info_books.keys())
print('books:',len(set(books)))
print('nonexistingbooks:',len(nonexistingbooks))
user = []
book = []
rating = []
for u in users:
    for b in ratings_users[u].keys():
        if b not in nonexistingbooks and ratings_users[u][b]!='0':
            user.append(u)
            book.append(b)
            r = ratings_users[u][b]
            rating.append(r)

# prova
print('prova:')
for i in range(0,10):
    print(user[i],book[i],rating[i])

# a questo punto creiamo un nuovo dataframe ratings
data = {}
data['User-ID'] = user
data['ISBN'] = book
data['Book-Rating'] = rating
newidxs = random.sample(range(len(user)),len(user))
d = pd.DataFrame(data, index = newidxs)
print('d.head()')
print(d.head())
print('d.shape[0]:')
print(d.shape[0])

# new data
step = int(len(newidxs)/5)
print('step:',step)
d1 = d.loc[list(range(0,step))]
d2 = d.loc[list(range(step,2*step))]
d3 = d.loc[list(range(2*step,3*step))]
d4 = d.loc[list(range(3*step,4*step))]
d5 = d.loc[list(range(4*step,d.shape[0]))]
print('len(d1,d2,d3,d4,d5):')
print(len(d1))
print(len(d2))
print(len(d3))
print(len(d4))
print(len(d5))
d1.to_csv('BR1(withoutzeros).csv', index = False, sep='\t', encoding='utf8')
d2.to_csv('BR2(withoutzeros).csv', index = False, sep='\t', encoding='utf8')
d3.to_csv('BR3(withoutzeros).csv', index = False, sep='\t', encoding='utf8')
d4.to_csv('BR4(withoutzeros).csv', index = False, sep='\t', encoding='utf8')
d5.to_csv('BR5(withoutzeros).csv', index = False, sep='\t', encoding='utf8')

print('users',len(users))
print('new nrows:',len(user))