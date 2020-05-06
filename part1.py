import os
import json
import re
from bs4 import BeautifulSoup

class Posting:
    def __init__(self, docid, tfidf, fields = ""):
        self.docid = docid
        self.tfidf = tfidf
        self.fields = fields


def tokenize(text):
    l = []
    for i in re.findall(r'[a-zA-Z0-9]{2,}', text):
        i = i.lower()
        l.append(i)
    return l


def computeWordFrequencies(tokens):
    freq_dict = {}
    for i in tokens:
        #if i not in stopwords:
        if i in freq_dict.keys():
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    return freq_dict

def build_index(a):
    table = {}
    urls = set()
    n = 0
    for i, b in enumerate(a):
        #print(b[0])
        if b[0] != 'DEV':
            something = os.listdir(b[0])
            for i in something:
                if i not in urls:
                    urls.add(i)
                    if len(urls) == 1:
                        print(i)
                        n += 1
                        data = json.load(open(b[0] + '/' + i))
                        txt = data['content']
                        soup = BeautifulSoup(txt, "html.parser")
                        text = soup.get_text()
                        tokens = computeWordFrequencies(tokenize(text))
                        for k,v in tokens.items():
                            if k not in table.keys():
                                p = Posting(n,v)
                                table[k] = [(p.docid, p.tfidf)]
                            else:
                                p = Posting(n,v)
                                table[k].append((p.docid, p.tfidf))
    return table

if __name__ == '__main__':
    a = os.walk('DEV')
    print(build_index(a))
