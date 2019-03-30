import time
import requests
import re
from bs4 import BeautifulSoup
alph = 'abcdefghijklmnoprstuvwxyz'
recipes = set() #ricette
i = 0
for letter in alph:
    print(letter)
    cnt = requests.get('http://www.bbc.co.uk/food/ingredients/by/letter/'+letter)
    soup = BeautifulSoup(cnt.text , 'lxml')
    ingredients = set() #ingredienti per ogni lettera
    for link in soup.find_all('img'):
        if(link.get('alt').startswith(letter)):
            ingredients.add(link.get('alt'))
    print(ingredients)
    print('n:', len(ingredients))
    for ingredient in ingredients:
        print('ingrediente:',ingredient)
        stop = False
        while stop == False:
            stop = True
            try:
                cnt = requests.get('http://www.bbc.co.uk/food/recipes/search?keywords='+ingredient)
            except:
                time.sleep(3)
                print('exception')
                stop = False
            if stop == True and str(cnt)!='<Response [200]>':
                time.sleep(3)
                stop = False
        soup = BeautifulSoup(cnt.text , 'lxml')
        pages = set()
        for page in soup.find_all('a'):
            if page.get('href').startswith('/food/recipes/search?page='):
                numpage = re.findall('[0-9]+',page.get('href'))[0]
                pages.add(int(numpage))
        if len(pages)>0:
            lastpage = sorted(pages)[-1]
        else:
            lastpage = 1
        print('npages:',lastpage)
        for page in range(1,lastpage+1):
            #print('ingrediente', ingredient)
            #print('page', page)
            #time.sleep(2)
            stop = False
            while stop == False:
                stop = True
                try:
                    cnt = requests.get('http://www.bbc.co.uk/food/recipes/search?page='+str(page)+'&keywords='+ingredient)
                except:
                    time.sleep(3)
                    print('exception')
                    stop = False
                if stop == True and str(cnt)!='<Response [200]>':
                    time.sleep(3)
                    stop = False
            soup = BeautifulSoup(cnt.text , 'lxml')
            for link in soup.find_all('a'):
                if(link.get('href').startswith('/food/recipes/')
                   and not link.get('href')=='/food/recipes/'
                   and 'search' not in link.get('href')):
                    recipes.add(link.get('href'))
                    #print(link.get('href'))
                    i += 1
        print(i)
        print('recipes:',len(recipes))

import pandas as pd
d = {'recipes': recipes}
df = pd.DataFrame(data=d)
df.to_csv('recipes.csv', index = False, sep='\t', encoding='utf8')
