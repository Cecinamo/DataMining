import pandas as pd
import numpy as np

BR1 = pd.read_csv('BR1.csv', sep='\t', encoding='utf8')
BR2 = pd.read_csv('BR2.csv', sep='\t', encoding='utf8')
BR3 = pd.read_csv('BR3.csv', sep='\t', encoding='utf8')
BR4 = pd.read_csv('BR4.csv', sep='\t', encoding='utf8')
BR5 = pd.read_csv('BR5.csv', sep='\t', encoding='utf8')
train1 = pd.concat([BR1,BR2,BR3,BR4], axis = 0, ignore_index = True)
train2 = pd.concat([BR2,BR3,BR4,BR5], axis = 0, ignore_index = True)
train3 = pd.concat([BR3,BR4,BR5,BR1], axis = 0, ignore_index = True)
train4 = pd.concat([BR4,BR5,BR1,BR2], axis = 0, ignore_index = True)
train5 = pd.concat([BR5,BR1,BR2,BR3], axis = 0, ignore_index = True)

import json
with open('ratings_users1.json') as data_file:    
    ratings_users1 = json.load(data_file)
with open('ratings_users2.json') as data_file:    
    ratings_users2 = json.load(data_file)
with open('ratings_users3.json') as data_file:    
    ratings_users3 = json.load(data_file)
with open('ratings_users4.json') as data_file:    
    ratings_users4 = json.load(data_file)
with open('ratings_users5.json') as data_file:    
    ratings_users5 = json.load(data_file)
with open('nearest1.json') as data_file:    
    nearest1 = json.load(data_file)
with open('nearest2.json') as data_file:    
    nearest2 = json.load(data_file)
with open('nearest3.json') as data_file:    
    nearest3 = json.load(data_file)
with open('nearest4.json') as data_file:    
    nearest4 = json.load(data_file)
with open('nearest5.json') as data_file:    
    nearest5 = json.load(data_file)
with open('mbooks.json') as data_file:    
    mbooks = json.load(data_file)
                   
train = [train1,train2,train3,train4,train5]
test = [BR5,BR1,BR2,BR3,BR4]
ratings_users = [ratings_users1,ratings_users2,ratings_users3,ratings_users4,ratings_users5]
nearest = [nearest1,nearest2,nearest3,nearest4,nearest5]
RMSE = []

# let's save the results on a text file
# (ratings estimated with mbooks)
out_file = open("ADM_cv-user-based3.txt","w")
out_file.write("CROSS-VALIDATION RESULTS:\n\n\n")

for i in range(5):

    print('cross-validation',i+1)
    string = 'cross-validation '+str(i+1)+':\n\n'
    out_file.write(string)
    
    
    f = 0
    n = 0
    scores = []
    
    for row in range(test[i].shape[0]):
    #for row in range(10):
        user = str(test[i]['User-ID'][row])
        book = str(test[i]['ISBN'][row])
        rating = test[i]['Book-Rating'][row]
        
        if rating!=0:
            notnull = True
            print()
            n+=1
            print('user:      book:     ratings:')
            print(user,book,rating)
            nearest_users = []
            if user in nearest[i].keys():
                nearest_users = set(nearest[i][user].keys()).difference(user)
            print('vicini:\n',nearest_users)
            ratings = []
            for nu in nearest_users:
                if book in ratings_users[i][nu].keys():
                    print('vicino:', nu, 'ha votato libro:',ratings_users[i][nu][book])
                    r = int(ratings_users[i][nu][book])
                    if r!=0:
                        ratings.append(r)
                    else:
                        ratings.append(mbooks['books'][book])
            # let's estimate the rating
            if len(ratings)>0:
                f+=1
                print('ratings:',ratings)
                r_hat = mbooks['books'][book]
                s = (r_hat-rating)**2
                scores.append(s)
                print(r_hat)

    print('scores:', scores)
    RMSE.append((np.mean(scores))**(0.5))
    print(RMSE[-1])
    print('books estimated with mbooks:',f)
    string = 'books estimated with mbooks: '+str(f)+'\n\n'+'RMSE: '+str(RMSE[-1])+'\n\n'
    out_file.write(string)

print(RMSE)
print(np.mean(RMSE))
string = 'FINAL RMSE: '+str(np.mean(RMSE))
out_file.write(string)