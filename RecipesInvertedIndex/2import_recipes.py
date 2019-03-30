import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
import extract as ex

import pandas as pd
recipes = pd.read_csv('recipes.csv')['recipes']

Id = []
title = []
author = []
preptime = []
cooktime = []
recipeyeld = []
dietary = []
ingredients = []
method = []

cont = 0
for r in recipes:
    cnt = requests.get('http://www.bbc.co.uk'+r)
    if str(cnt) == '<Response [404]>':
        print('Error 404 founded! ')
        continue
    j = 0
    while str(cnt) != '<Response [200]>':
            time.sleep(1)
            print('sleeping')
            print(r, str(cnt))
            if j == 10:
                break
            j += 1
            cnt = requests.get('http://www.bbc.co.uk'+r)   
    soup = BeautifulSoup(cnt.text , 'lxml')
    title.append(str(soup.title)[28:-8])
    Idrecipe = (re.findall('[0-9]+', r))
    Id.append(Idrecipe[0])
    author.append(ex.extractGenericInfo(soup, 'author'))
    preptime.append(ex.extractGenericInfo(soup, 'prepTime'))
    cooktime.append(ex.extractGenericInfo(soup, 'cookTime'))
    recipeyeld.append(ex.extractGenericInfo(soup, 'recipeYield'))
    dietary.append(ex.extractDietary(soup))
    ingredients.append(ex.extractComplexInfo(soup, 'ingredients'))
    method.append(ex.extractMethod(soup))
    cont += 1
    print(cont, title[-1])
    
d = {'Id': Id, 'title': title, 'author': author, 'preptime': preptime, 'cooktime': cooktime, 'recipeyeld': recipeyeld, 
      'dietary': dietary, 'ingredients': ingredients, 'method': method}
df = pd.DataFrame(data=d)
df.to_csv('recipes_info_complete.csv', index = False, sep='\t', encoding='utf8')
print('done')
