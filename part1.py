import os
import json
import re
from bs4 import BeautifulSoup
import pickle
from decimal import Decimal

stopwords = set()

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
        if i not in stopwords:
            if i in freq_dict.keys():
                freq_dict[i] += 1
            else:
                freq_dict[i] = 1
    return freq_dict

def build_index(a):
    table = {}
    urls = set()
    n = 0

    for ii, b in enumerate(a):
        #print(b[0])
        #print(str(b[0]) + "__________")
        if b[0] != 'DEV':

            something = os.listdir(b[0])
            for i in something:
                print(str(round(Decimal(n/55393),3)*100) + "% done, on file number " + str(n))
                if i not in urls:
                    urls.add(i)

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
                    if n%5000 == 0:
                        pickle.dump(table, open('disk/disk' + str(n) + '.pickle', 'wb'))
                        table.clear()
                        print(pickle.load(open('disk/disk' + str(n) + '.pickle', 'rb')))
    pickle.dump(table, open('disk/disk' + str(n) + '.pickle', 'wb'))
    table.clear()
    print("DONE")
    return table

if __name__ == '__main__':
    f = open("stopwords.txt")
    for line in f:
        stopwords.add(line.strip("\n"))
    f.close()
    print(stopwords)
    a = os.walk('DEV')
    result = build_index(a)





    # for k,v in result.items():
    #     print(k,v)




    # hi = [1,2,3]
    # pickle.dump(hi, open('gamestate.pickle', 'wb'))
    # diskstuff = pickle.load(open('gamestate.pickle', 'rb'))
    # print(diskstuff)
