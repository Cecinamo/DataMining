
import numpy as np
import re

def user_profile(user,mbooks,info_books):
    up = {}
    # for each rated book (if it exist)
    for book in user.keys():
        if book in info_books.keys():
            if user[book]=='0':
                user[book] = float(mbooks['books'][book])
                #user[book] = np.mean([int(v) for v in user.values() if v!=0])
            for k in info_books[book].keys():
                s = info_books[book][k]
                if k=='book-title':
                    s = s.split()
                else:
                    s = [s]
                # some weigths
                if k=='book-title':
                    s = s*2
                if k=='book-author':
                    s = s*2
                for w in s:
                    if w in up.keys():
                        up[w]+=[int(user[book])]
                    else:
                        up[w]=[int(user[book])]
    for w in up.keys():
        up[w] = np.mean(up[w])
    return(up)

def vecusers(u,cwords):
    v = []
    # for each word in common words
    for w in cwords:
        # if the user contains the word, we add the value to the vector
        if w in u.keys():
            v.append(float(u[w]))
        # otherwise we add zero
        else:
            v.append(0)
    return(np.array(v))

def vecbooks(b,cwords):
    v = []
    for w in cwords:
        # if the book contains the word, we add the value to the vector
        if w in b.values():
            v.append(1)
        # otherwise we add zero
        else:
            v.append(0)
    return(np.array(v))

def cos_similarity(a,b):
    return(np.inner(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

def recommended(user,info_books,mbooks,info):
    up = user_profile(user,mbooks,info_books)
    r = {}
    b = []
    d = []
    for book in info_books.keys():
        if book not in user.keys():
            # we have to split the title
            bookwords = []
            for k in info_books[book].keys():
                w = info_books[book][k]
                if k=='book-title':
                    w = w.split()
                else:
                    w = [w]
                bookwords += w
            cwords = set(up.keys()).union(bookwords)
            if len(cwords)>0 and len(up.values())>0:
                #print(users_profiles[user].values())
                b.append(book)
                vu = vecusers(up,cwords)
                vb = vecbooks(info_books[book],cwords)
                #print('vu',vu)
                #print('vb',vb)
                dis = cos_similarity(vu,vb)
                d.append(dis)
    idxs = list(np.argsort(np.array(d))[-20:]) # let's keep only 10 items
    idxs.reverse()
    for i in idxs: 
        r[b[i]]=str(d[i])
    # we will print only 10 books
    n = 0
    original_titles = []
    original_authors = []
    nb = len(user.keys())+len(idxs)
    # let's save all the titles and the authors of the books
    for i in idxs:
        original_titles.append(re.sub(' ','',info[b[i]]['Book-Title'].lower()))
        original_authors.append(re.sub(' ','',info[b[i]]['Book-Author'].lower()))
    for book in user.keys():
        original_titles.append(re.sub(' ','',info[book]['Book-Title'].lower()))
        original_authors.append(re.sub(' ','',info[book]['Book-Author'].lower()))
    for i in idxs:
        stop = False
        c = i+1
        while stop==False and c<nb:
            if(re.sub(' ','',info[b[i]]['Book-Title'].lower())==original_titles[c] and re.sub(' ','',info[b[i]]['Book-Author'].lower())==original_authors[c]):
                stop = True
            c+=1
        if stop==False and n<10:
            print('\n')
            print('ISBN:',b[i])
            print('TITLE:',info[b[i]]['Book-Title'],'AUTHOR:',info[b[i]]['Book-Author'],
                  'YOP:',info[b[i]]['Year-Of-Publication'],'PUBLISHER:',info[b[i]]['Publisher'])
            n+=1
    return(r)