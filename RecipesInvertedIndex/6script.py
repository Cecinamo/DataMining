import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
import operator
#nltk.download("stopwords")
print('Program is running, wait just a bit...')
vector = pd.read_csv('vettorepesato.csv', sep='\t', encoding='utf8')
print('file 1/3 uploaded')
inverted = pd.read_csv('invidxpesato.csv', sep='\t', encoding='utf8')
print('file 2/3 uploaded')
info = pd.read_csv('recipes_info_complete.csv', sep='\t', encoding = 'utf8')
print('file 3/3 uploaded')
print('\n')

# indici ricettaid-posizione
idxs = {}
for i in range(info.shape[0]):
    idxs[str(info['Id'][i])] = i

# ordine stampa
orderedprint = ['title', 'author', 'dietary', 'recipeyeld', 'cooktime', 'preptime', 'ingredients', 'method']

def cos_similarity(a,b):
    return(np.inner(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))

# inizio


def fastrecipes(recipes):
    for i in recipes.copy():
        if len(re.findall('hour',str(info['preptime'][i])))>0:
            recipes.discard(i)
    return recipes

def vegetarian(recipes):
    decision = '_'
    while decision == '_':
        decision = input('Press 1 for vegetarian recipes, otherwise press ENTER: ')
        if decision == '1':
            for i in recipes.copy():
                if info['dietary'][idxs[i]] is np.nan:
                    recipes.discard(i)
        elif len(decision) == 0:
            pass
        else:
            print('Invalid input, try again')
            decision = '_'
    
    return recipes

def fastrecipes(recipes):
    decision = '_'
    while decision == '_':
        decision = input('Press 1 for fast recipes, otherwise press ENTER: ')
        if decision == '1':
            for i in recipes.copy():
                if len(re.findall('hour',str(info['preptime'][idxs[i]])))>0:
                    recipes.discard(i)
        elif len(decision) == 0:
            pass
        else:
            print('Invalid input, try again')
            decision = '_'
    
    return recipes


stop = False
while stop==False:
    

    search = input('What would you like to cook?')
    if len(search)>0:
        #pulizia stringa
        sw = stopwords.words('english')
        #print(sw)
        search = search.lower()
        search = re.findall('[a-z]+', search)
        searchwords = []
        for i in search:
            if i not in sw:
                searchwords.append(nltk.PorterStemmer().stem_word(i))
        #print(searchwords)
        # creiamo il vettore
        v = []
        searchwords = ' '.join(searchwords)
        for i in vector['words']:
            n = len(re.findall(' '+str(i)+' ', ' '+searchwords+' '))
            v.append(n)
            #if n>0:
                #print(i)
        v = np.array(v)
        #print(v)
        # ricette che contengono le parole
        recipes = []
        for i in searchwords.split():
            if i in inverted.keys():
                recipes += str(inverted[i].values[0]).split()
        
        recipes = fastrecipes(set(recipes))
        recipes = vegetarian(recipes)
        
        
            
        
        if len(recipes)==0:
            print('no recipe found.')
        else:
            #print('recipes', recipes)
            # cosine similarity
            cos = {}
            for j in recipes:
                cos[j] = cos_similarity(v,vector[j])
            #print(cos)
            sorted_r = [i for i,j in sorted(cos.items(), key=operator.itemgetter(1), reverse = True)]
            #print(sorted_r)
            orderedrecipes = []
            for i in range(min(20,len(sorted_r))):
                orderedrecipes.append(idxs[sorted_r[i]])
                print(str(i)+':', info['title'][orderedrecipes[-1]])
            # scelta della ricetta
            stop2 = False
            while stop2 == False:
                rec = input('which one do you prefer? [press enter to stop]')
                if len(rec)>0:
                    try:
                        rec = int(rec)
                        if rec>=0 and rec<len(orderedrecipes):
                            for k in orderedprint:
                                p = info[k][orderedrecipes[rec]]
                                if str(p)!= 'nan':
                                    print(str(k).upper()+':')
                                    print(p)
                        else:
                            print('invalid index')
                    except ValueError:
                        print('invalid index')
                else:
                    stop2 = True
    else:
        stop = True