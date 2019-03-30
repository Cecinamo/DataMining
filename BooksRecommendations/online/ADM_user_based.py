import numpy as np
def cos_similarity(a,b):
    return(np.inner(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

# vettore
# deve avere come minimo di componenti le componenti non nulle per tutti e due gli utenti (common books)
def vec(b,cbooks,mbooks):
    v = []
    # per ogni libro in common books
    for book in cbooks:
        #print(book in Books['ISBN'])
        #if book in set(Books['ISBN']):
            #print(book)
        # se il libro e' stato votato dall'utente, aggiungi il voto
        # se il voto e' zero usa come voto il voto medio del libro
        if book in b.keys():
            if str(b[book])!='0':
                v.append(int(b[book]))
            else:
                v.append(mbooks['books'][book])
        # altrimenti aggiungi zero
        else:
            v.append(0)
    return(np.array(v))

def fnearest_users(user, ratings_books, ratings_users, mbooks):
    # vediamo quali libri ha votato
    books1 = user
    #print('libri votati da utente:',list(books1.keys()))
    #print('voti:', list(books1.values()))
    # vediamo quali altri utenti hanno votato gli stessi libri
    nearest_users = []
    for book in books1.keys():
        # se il libro e' stato votato 
        if book in ratings_books.keys():
            nearest_users += ratings_books[book].keys()
    #print('nearest_users',nearest_users)
    # per ognuno di questi devo calcolare la distanza da user
    nearest = {}
    u2 = []
    dist = []
    for user2 in nearest_users:
        # se questo vicino non ha votato niente a parte questo libro, non ce ne facciamo molto..
        if len(ratings_users[user2].keys())>10:
            # mi serve il suo vettore dei voti a cui devo aggiungere anche i libri di user (common books) 
            books2 = ratings_users[user2]
            cbooks = list(set(books2.keys()).union(books1.keys()))
            #print(cbooks)
            v1 = vec(books1,cbooks,mbooks)
            v2 = vec(books2,cbooks,mbooks)
            #print('v1',v1)
            #print('v2',v2)
            d = cos_similarity(v1,v2)
            #print(user2, d)
            u2.append(user2)
            dist.append(d)
    idxs = np.argsort(np.array(dist))[-10:] #ce ne teniamo solo 50
    for i in idxs: nearest[u2[i]]=str(dist[i])
    return nearest

def user_based(user,ratings_books,ratings_users,mbooks,info):
    # devo trovare i suoi vicini
    nearest = fnearest_users(user, ratings_books, ratings_users,mbooks)
    #print(nearest)
    # e con i vicini stimare i ratings per gli altri libri
    # gli altri libri pero' che sono stati votati da almeno un vicino
    # ma non dallo user
    books = []
    for nuser in nearest.keys():
        #print('user:',nuser)
        for book in ratings_users[nuser]:
            #print('ha votato:',book)
            books.append(book)
    #print(books)
    books = list(set(books).difference(user.keys()))
    #print(books)
    recommended = {}
    ratings_hat = []
    for book in books:
        ratings = []
        for nuser in nearest.keys():
            if book in ratings_users[nuser].keys():
                if ratings_users[nuser][book]!='0':
                    r = int(ratings_users[nuser][book])
                else:
                    r = mbooks['books'][book]
                ratings.append(r)
                #print('ratings:',ratings)
        ratings_hat.append(np.mean(ratings))
    #print('ratings:',ratings_hat)
    idxs = list(np.argsort(np.array(ratings_hat))[-20:])
    idxs.reverse()
    #print('idxs:',idxs)
    for i in idxs: recommended[books[i]]=str(ratings_hat[i])

    #print('teoricamente ha finito')
    # ne stampiamo solo 10 in cui però titolo e autore sono diversi da quelli originali
    n = 0
    # titoli e autori originali
    original_titles = []
    original_authors = []
    nb = len(user.keys())+len(idxs)
    # salvo tutti i titoli e gli autori dei libri
    for i in idxs:
        original_titles.append(info[books[i]]['Book-Title'].lower())
        original_authors.append(info[books[i]]['Book-Author'].lower())
    for book in user.keys():
        original_titles.append(info[book]['Book-Title'].lower())
        original_authors.append(info[book]['Book-Author'].lower())
    for i in idxs:
        stop = False
        c = i+1
        while stop==False and c<nb:
            if(info[books[i]]['Book-Title'].lower()==original_titles[c] and info[books[i]]['Book-Author'].lower()==original_authors[c]):
                stop = True
            c+=1
        if stop==False and n<10:
            print('\n')
            #print('rating_hat',ratings_hat[i])
            print('ISBN:',books[i])
            print('TITLE:',info[books[i]]['Book-Title'],'AUTHOR:',info[books[i]]['Book-Author'],
                  'YOP:',info[books[i]]['Year-Of-Publication'],'PUBLISHER:',info[books[i]]['Publisher'])
            n+=1
    return recommended