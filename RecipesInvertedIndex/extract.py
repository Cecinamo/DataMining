def extractGenericInfo(soup, item):
    result = ""
    for tag in soup.find_all(itemprop=item):
        result= tag.contents[0]
    return result
def extractComplexInfo(soup, itemtype):
    result = []
    for tag in soup.find_all(itemprop=itemtype):
        result.append(tag.text.strip())
    return ' '.join(result)
def extractDietary(soup):
    result = ''
    for p in soup.find_all('p'):
        if(str(p.get('class')).startswith('[\'recipe-metadata__dietary')):
            result = p.text.strip()
            break
    return result
def extractMethod(soup):
    result = ''
    for p in soup.find_all('p'):
        if(str(p.get('class'))=='[\'recipe-method__list-item-text\']'):
            result += p.text.strip()+'\n'
    return result
