import pandas as pd
import re
import numpy as np
pulizie = pd.read_csv('pulizie.csv', sep='\t', encoding='utf8')
tutteleparoledelmondo = set()
for i in range(pulizie.shape[0]):
    for j in ['method', 'ingredients', 'title']:
        w = str(pulizie[j][i]).split()
        for k in w:
            tutteleparoledelmondo.add(k)
            
tutteleparoledelmondo = sorted(list(tutteleparoledelmondo))
print(tutteleparoledelmondo)
print(len(tutteleparoledelmondo))



d = {}
d['words'] = tutteleparoledelmondo
print(d['words'])
for i in range(pulizie.shape[0]):
    values = []
    app = ' '.join([(str(pulizie['title'][i])+' ')*10,str(pulizie['ingredients'][i]),str(pulizie['method'][i])])
    for j in tutteleparoledelmondo:
        values.append(len(re.findall(' '+j+' ',' '+app+' ')))
    d[str(pulizie['id'][i])] = np.array(values)
    print(i, len(values))
df = pd.DataFrame(data=d)
df.to_csv('vettorepesato.csv', index = False, sep='\t', encoding='utf8')