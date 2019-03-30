# inverted index
import pandas as pd
import re
import numpy as np
vect = pd.read_csv('vettorepesato.csv', sep='\t', encoding='utf8')
d = {}
for i in range(vect.shape[0]):
    print(i, vect['words'][i])
    values = []
    for j in vect.keys()[:-1]:
        if vect[j][i]>0:
            values.append(j)
    d[str(vect['words'][i])] = [' '.join(values)]

df = pd.DataFrame(data=d)
df.to_csv('invidxpesato.csv', index = False, sep='\t', encoding='utf8')
