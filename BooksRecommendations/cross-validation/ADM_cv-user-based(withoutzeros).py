import pandas as pd
import numpy as np

BR1 = pd.read_csv('BR1(withoutzeros).csv', sep='\t', encoding='utf8')
BR2 = pd.read_csv('BR2(withoutzeros).csv', sep='\t', encoding='utf8')
BR3 = pd.read_csv('BR3(withoutzeros).csv', sep='\t', encoding='utf8')
BR4 = pd.read_csv('BR4(withoutzeros).csv', sep='\t', encoding='utf8')
BR5 = pd.read_csv('BR5(withoutzeros).csv', sep='\t', encoding='utf8')
train1 = pd.concat([BR1,BR2,BR3,BR4], axis = 0, ignore_index = True)
train2 = pd.concat([BR2,BR3,BR4,BR5], axis = 0, ignore_index = True)
train3 = pd.concat([BR3,BR4,BR5,BR1], axis = 0, ignore_index = True)
train4 = pd.concat([BR4,BR5,BR1,BR2], axis = 0, ignore_index = True)
train5 = pd.concat([BR5,BR1,BR2,BR3], axis = 0, ignore_index = True)

def ratings_books_users(BR):
    ratings_books = {}
    ratings_users = {}
    for i in range(BR.shape[0]):
        #print(i)
        rb = {}
        ru = {}
        user = BR['User-ID'][i]
        book = BR['ISBN'][i]
        rating = BR['Book-Rating'][i]
        rb[user] = rating
        ru[book] = rating
        if book in ratings_books.keys():
            ratings_books[book].update(rb)
        else:
            ratings_books[book] = rb
        if user in ratings_users.keys():
            ratings_users[user].update(ru)
        else:
            ratings_users[user] = ru
    return ratings_books,ratings_users

# NEAREST USERS
# dobbiamo trovare gli utenti piu' vicini agli utenti che fanno parte del test

def cos_similarity(a,b):
    return(np.inner(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

# vettore
# deve avere come minimo di componenti le componenti non nulle per tutti e due gli utenti (common books)
def vec(b,cbooks):
    v = []
    # per ogni libro in common books
    for book in cbooks:
        #print(book in Books['ISBN'])
        #if book in set(Books['ISBN']):
            #print(book)
        # se il libro e' stato votato dall'utente, aggiungi il voto
        if book in b.keys():
            v.append(b[book])
        # altrimenti aggiungi zero
        else:
            v.append(0)
    return(np.array(v))

def fnearest_users(users, ratings_books, ratings_users):
    print('fnearest_users')
    print(len(users))
    nearest = {}
    n = 0
    for user1 in users:
        # se lo abbiamo anche nel train
        if user1 in ratings_users.keys():
            # vediamo quali libri ha votato
            books1 = ratings_users[user1]
            print(n)
            n+=1
            #print('libri votati da utente '+str(user1)+':',list(books1.keys()))
            #print('voti:', list(books1.values()))
            # vediamo quali altri utenti hanno votato gli stessi libri
            nearest_users = []
            for book in books1.keys():
                nearest_users += ratings_books[book].keys()
            #print('nearest_users',nearest_users)
            # per ognuno di questi devo calcolare la distanza da user
            nu = {}
            u2 = []
            dist = []
            for user2 in nearest_users:
                if len(ratings_users[user2].keys())>20:
                    # mi serve il suo vettore dei voti a cui devo aggiungere anche i libri di user (common books) 
                    # (e tolgo quelli che non esistono nella lista di Books)
                    books2 = ratings_users[user2]
                    cbooks = list(set(books2.keys()).union(books1.keys()))
                    #print(cbooks)
                    v1 = vec(books1,cbooks)
                    v2 = vec(books2,cbooks)
                    #print('v1',v1)
                    #print('v2',v2)
                    d = cos_similarity(v1,v2)
                    #print(user2, d)
                    if user2!=user1:
                        u2.append(user2)
                        dist.append(d)
            idxs = np.argsort(np.array(dist))[-20:] #ce ne teniamo solo 20
            for i in idxs: nu[u2[i]]=str(dist[i])
            nearest[user1] = nu
            #print(nearest[user1])
    return nearest

import json
with open('mbooks.json') as data_file:    
    mbooks = json.load(data_file)

train = [train1,train2,train3,train4,train5]
test = [BR5,BR1,BR2,BR3,BR4]

RMSE = []

# salviamo i risultati su un file di testo
out_file = open("ADM_cv-user-based(without-zeros).txt","w")
out_file.write("CROSS-VALIDATION RESULTS:\n\n\n")

for i in range(5):

    print('cross-validation',i+1)
    string = 'cross-validation '+str(i+1)+':\n\n'
    out_file.write(string)
    
    test_users = set(test[i]['User-ID'])
    ratings_books, ratings_users = ratings_books_users(train[i])
    nearest = fnearest_users(test_users,ratings_books,ratings_users)
    
    # ora abbiamo tutti gli utenti vicini ai nostri utenti del test
    # per ogni riga del test set dobbiamo vedere utente e libro di cui prevedere il voto
    # facendo la media dei voti che hanno dato i suoi vicini a quel libro
    
    f = 0
    scores = []
    
    for row in range(test[i].shape[0]):
        user = test[i]['User-ID'][row]
        book = test[i]['ISBN'][row]
        rating = test[i]['Book-Rating'][row]
        #print(user,book,rating)
        # troviamo i vicini di user
        nearest_users = []
        if user in nearest.keys():
            nearest_users = list(nearest[user].keys())
        #print('vicini:\n',nearest_users)
        # troviamo i voti dei vicini per book
        ratings = []
        for nu in nearest_users:
            if book in ratings_users[nu].keys():
                r = ratings_users[nu][book]
                ratings.append(r)
        #print('voti:\n',ratings)
        # stimiamo il voto
        if len(ratings)>0:
            r_hat = np.mean(ratings)
        elif book in mbooks['books'].keys():
            f+=1
            r_hat = mbooks['books'][book]
        else:
            print('e\' andata male')
            r_hat = 6
        #print(r_hat)
        s = (r_hat-rating)**2
        scores.append(s)

    RMSE.append((np.mean(scores))**(0.5))
    print(RMSE[-1])
    print('libri stimati con mbooks:',f,'   su:',test[i].shape[0])
    string = 'books estimated with mbooks: '+str(f)+'   over: '+str(test[i].shape[0])+'\n\n'+'RMSE: '+str(RMSE[-1])+'\n\n'
    out_file.write(string)

print(RMSE)
print(np.mean(RMSE))
string = 'FINAL RMSE: '+str(np.mean(RMSE))
out_file.write(string)