import ADM_content_based as cb
import ADM_user_based as ub
import ADM_item_based as ib
import json
import csv

with open('info_books(original).json') as data_file:    
    info = json.load(data_file)
with open('mbooks.json') as data_file:    
    mbooks = json.load(data_file)
with open('info_books.json') as data_file:    
    info_books = json.load(data_file)
with open('ratings_users(cleaned).json') as data_file:    
    ratings_users = json.load(data_file)
with open('ratings_books(cleaned).json') as data_file:    
    ratings_books = json.load(data_file)
with open('books_distances.json') as data_file:
    books_distances = json.load(data_file)

stop = False
while stop==False:
    filename = input('inserire nome file: ')
    # prova.tsv
    if len(filename)>0:
        user = {}
        with open(filename) as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for line in tsvreader:
                user[line[0]] = line[1]
        #print(user)
        for book in user.keys():
            print('TITLE:',info[book]['Book-Title'],'AUTHOR:',info[book]['Book-Author'],
                  'YOP:',info[book]['Year-Of-Publication'],'PUBLISHER:',info[book]['Publisher'])
            print('RATING:',user[book],'\n')
        print('\n------------------------------------------------------------------------------------------------------------------------------------------\n')
        print('ITEM BASED RECOMMENDATIONS')
        print('\n------------------------------------------------------------------------------------------------------------------------------------------')
        IBR = ib.item_based(user, books_distances, mbooks, info)
        print('\n------------------------------------------------------------------------------------------------------------------------------------------\n')
        print('USER BASED RECOMMENDATIONS')
        print('\n------------------------------------------------------------------------------------------------------------------------------------------')
        UBR = ub.user_based(user,ratings_books,ratings_users,mbooks,info)
        print('\n------------------------------------------------------------------------------------------------------------------------------------------\n')
        print('CONTENT BASED RECOMMENDATIONS')
        print('\n------------------------------------------------------------------------------------------------------------------------------------------')
        CBR = cb.recommended(user,info_books,mbooks,info)
    else:
        stop = True