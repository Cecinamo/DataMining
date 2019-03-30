from operator import itemgetter

def item_based(user, books_distances, mbooks, info):
    best_books = []
    suggested_books = {}
    n = 0
    for isbn in user.keys():
        for book in books_distances[isbn]:
            if isbn in books_distances[book]:
                suggested_books[book] = int(user[isbn])
    sorted_books = sorted(suggested_books.items(), key=itemgetter(1), reverse = True)
    for i in sorted_books:
        best_books.append(i[0])
    original_titles = []
    original_authors = []
    nb = len(user.keys()) + len(best_books)
    for i in best_books:
        original_titles.append(info[i]['Book-Title'].lower())
        original_authors.append(info[i]['Book-Author'].lower())
    for book in user.keys():
        original_titles.append(info[book]['Book-Title'].lower())
        original_authors.append(info[book]['Book-Author'].lower())
    for i in range(len(best_books)):
        stop = False
        c = i + 1
        while stop == False and c < nb:
            if (info[best_books[i]]['Book-Title'].lower() == original_titles[c] and info[best_books[i]]['Book-Author'].lower() ==
                original_authors[c]):
                stop = True
            c += 1
        if stop == False and n < 10:
            print('\n')
            print('ISBN:', best_books[i])
            print('TITLE:', info[best_books[i]]['Book-Title'], 'AUTHOR:', info[best_books[i]]['Book-Author'],
                  'YOP:', info[best_books[i]]['Year-Of-Publication'], 'PUBLISHER:', info[best_books[i]]['Publisher'])
            n += 1
    return  best_books