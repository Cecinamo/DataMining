import pandas as pd
import json
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

with open('mbooks.json') as data_file:
    mbooks = json.load(data_file)

with open('books_distances.json') as data_file:
    books_distances = json.load(data_file)

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

ratings_users = [ratings_users1, ratings_users2, ratings_users3, ratings_users4, ratings_users5]
BR = [BR5, BR1, BR2, BR3, BR4, BR4]
RMSE = []

out_file = open("ADM_cv-item-based1.txt","w")
out_file.write("CROSS-VALIDATION RESULTS:\n\n\n")

for t in range(5):
    n = 0
    f = 0
    print('cross-validation', t + 1)
    string = 'cross-validation ' + str(t + 1) + ':\n\n'
    out_file.write(string)

    cnt = 0 #counter per il for
    score = []
    for i in BR[t]['ISBN'][:]:
        if BR[t]['Book-Rating'][cnt] == 0:
            cnt += 1
            continue
        n+=1
        if str(BR[t]['User-ID'][cnt]) in ratings_users[t].keys():
            #    if BR5['User-ID'][cnt] in books_distances:
            #    print('Similar books:', books_distances[i])
            #        print(ratings_users1[BR5['User-ID'][cnt]].keys())
            val = 0
            k = 0
#            print('User Number: ', BR[t]['User-ID'][cnt])
#            print('ISBN of the chosen book:' , i )
#            print('SIMILAR BOOKS')
            for j in books_distances[i].keys():
                if j in ratings_users[t][str(BR[t]['User-ID'][cnt])].keys():
                    if ratings_users[t][str(BR[t]['User-ID'][cnt])][j] != '0':
            #                    val += float(mbooks['books'][j])
            #                    val += np.mean([int(v) for v in ratings_users[str(BR5['User-ID'][cnt])].values() if v!='0'])
                        val += float(ratings_users[t][str(BR[t]['User-ID'][cnt])][j])
#                        print('ISBN:', j , 'Rated by user:', ratings_users[t][str(BR[t]['User-ID'][cnt])][j])
                    k += 1
            if k == 0 :
                f+=1
                val += float(mbooks['books'][i])
#                print('NONE')
#                print('Mean value of from user\'s preferences:', val)
                k += 1
            mean = val/k
            if np.isnan(mean):
                mean = float(mbooks['books'][i])

#            print('Rating assigned from user:' , BR[t]['Book-Rating'][cnt])
#            print('Value estimated:', mean)
#            print('Errore:', error)
#        else:
#            print('User doesn\'t exist')

        else:
            mean = float(mbooks['books'][i])
        error = (mean - float(BR[t]['Book-Rating'][cnt]))**2
#       print('Error:', error)
        score.append(error)
        cnt += 1
    RMSE.append((np.mean(score))**0.5)
    print('RMSE:', RMSE[-1])
    string = 'books estimated with mbooks: '+str(f)+'   over: '+str(n)+'\n\n'+'RMSE: '+str(RMSE[-1])+'\n\n'
    out_file.write(string)

print(RMSE)
print(np.mean(RMSE))
string = 'FINAL RMSE: '+str(np.mean(RMSE))
out_file.write(string)