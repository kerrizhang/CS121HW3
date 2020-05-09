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
    testing = False

    if not testing:
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
                            table_list = sorted(table.items())
                            pickle.dump(table_list, open('disk/mergefile' + str(n) + '.pickle', 'wb'))

                            table.clear()
        table_list = sorted(table.items())
        pickle.dump(table_list, open('disk/mergefile' + str(n) + '.pickle', 'wb'))
        table.clear()
        print("DONE")

    FINAL_INDEX = []

    diskfiles = os.listdir('disk')

    for picklefile in diskfiles:
        print("****** testing " + str(picklefile))
        #FINAL_INDEX = [('2007', [(99999, 2)]), ('30000', [(69, 1)])]
        final_i = 0
        second_i = 0
        #second_pickle_file = test_list
        second_pickle_file = pickle.load(open('disk/' + str(picklefile), 'rb'))

        while final_i < len(FINAL_INDEX) and second_i < len(second_pickle_file):
            #print(second_pickle_file)
            #print(type(second_pickle_file))
            #print(FINAL_INDEX)
            #print("WITH INDEX SECOND_I: ")
            #print(second_pickle_file[second_i])
            #print("index [0]: ")
            #print(second_pickle_file[second_i][0])
            if (FINAL_INDEX[final_i][0] == second_pickle_file[second_i][0]):
                for x in second_pickle_file[second_i][1]:
                    FINAL_INDEX[final_i][1].append(x)
                final_i += 1
                second_i += 1

            elif (FINAL_INDEX[final_i][0] < second_pickle_file[second_i][0]):
                final_i += 1
            else:
                FINAL_INDEX.insert(final_i, second_pickle_file[second_i])
                final_i += 1
                second_i += 1

        if final_i == len(FINAL_INDEX):
            if second_i == len(second_pickle_file):
                pass
            else:
                FINAL_INDEX.extend(second_pickle_file[second_i:])
    pickle.dump(FINAL_INDEX, open('final_index.pickle', 'wb'))
    f = open("results.txt", "a")
    for thing in FINAL_INDEX:
        f.write(thing)
        f.write("\n")
    f.close()
    return FINAL_INDEX



if __name__ == '__main__':
    empty_dict = dict()
    #empty_dict = pickle.load(open(empty_dict, 'disk/disk5000.pickle', 'rb'))
    pickle.dump(empty_dict, open('disk/mergefile.pickle', 'wb'))
    f = open("stopwords.txt")
    for line in f:
        stopwords.add(line.strip("\n"))
    f.close()
    print(stopwords)
    a = os.walk('DEV')
    result = build_index(a)
    print(result)
    #test([('2007', [(9, 2), (51, 2), (58, 1), (99, 3)]), ('2010', [(67, 1)]), ('2011', [(6, 1)])])






    # for k,v in result.items():
    #     print(k,v)




    # hi = [1,2,3]
    # pickle.dump(hi, open('gamestate.pickle', 'wb'))
    # diskstuff = pickle.load(open('gamestate.pickle', 'rb'))
    # print(diskstuff)
