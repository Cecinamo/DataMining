import pandas as pd
info = pd.read_csv('recipes_info_complete.csv', sep='\t', encoding='utf8')
import nltk
import re
from nltk.corpus import stopwords
#nltk.download("stopwords")
sw = stopwords.words('english')
#print(sw)
wm = []
wi = []
wt = []
for i in range(info.shape[0]):
    # method
    rm = str(info['method'][i]).lower()
    rm = re.findall('[a-z]+', rm)
    app = []
    for j in rm:
        if j not in sw:
            app.append(nltk.PorterStemmer().stem_word(j))
    wm.append(' '.join(app))
    # ingredients
    ri = str(info['ingredients'][i]).lower()
    ri = re.findall('[a-z]+', ri)
    app = []
    for j in ri:
        if j not in sw:
            app.append(nltk.PorterStemmer().stem_word(j))
    wi.append(' '.join(app))
    # title
    rt = str(info['title'][i]).lower()
    rt = re.findall('[a-z]+', rt)
    app = []
    for j in rt:
        if j not in sw:
            app.append(nltk.PorterStemmer().stem_word(j))
    wt.append(' '.join(app))
import pandas as pd
d = {'id': info['Id'], 'method': wm, 'ingredients': wi, 'title': wt}
df = pd.DataFrame(data=d)
df.to_csv('pulizie.csv', index = False, sep='\t', encoding='utf8')
