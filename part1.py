import os
import json
import re
from bs4 import BeautifulSoup
import pickle
from decimal import Decimal
import requests

# import timer

stopwords = set()


class Posting:
    def __init__(self, docid, tfidf, fields=""):
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
    docLength = {}
    urls = set()
    realurls = set()
    n = 0
    d = {}
    testing = False
    first = True

    simhash_set = set()

    if not testing:
        for ii, b in enumerate(a):
            # print(b[0])
            # print(str(b[0]) + "__________")
            if b[0] != 'DEV':

                something = os.listdir(b[0])
                for x in something:
                    i = x
                    print(str(round(Decimal(n / 55393), 3) * 100) + "% done, on file number " + str(n))

                    # Defragmentalize
                    if "#" in i:
                        i = i[:i.find('#')]
                    # print(i)
                    if i not in urls:
                        urls.add(i)

                        n += 1

                        data = json.load(open(b[0] + '/' + i))
                        txt = data['content']
                        # d[n] = data['url']
                        tempurl = data['url']
                        if "#" in tempurl:
                            tempurl = tempurl[:tempurl.find('#')]
                        d[n] = tempurl

                        if tempurl not in realurls:
                            realurls.add(tempurl)
                            try:
                                if requests.head(tempurl).status_code == 200:

                                    soup = BeautifulSoup(txt, "html.parser")
                                    text = soup.get_text(separator=" ")
                                    sizeOfPage = len(text)

                                    normaltokens = tokenize(text)
                                    docLength[n] = sizeOfPage

                                    tokens = computeWordFrequencies(normaltokens)
                                    # print(sorted(tokens))

                                    simhash_value = simhash(tokens)
                                    if simhash_value not in simhash_set:
                                        # DOUBLING THE POINTS FOR TITLE, HEADERS, AND BOLD TEXT HERE:
                                        for tag in soup.find_all("title"):
                                            for word in tokenize(tag.get_text(separator=" ")):
                                                if word not in stopwords:
                                                    tokens[word] = tokens[word] + 0.5
                                        for tag in soup.find_all(re.compile('^h[1-9]$')):
                                            for word in tokenize(tag.get_text(separator=" ")):
                                                if word not in stopwords:
                                                    tokens[word] = tokens[word] + 0.3
                                        for tag in soup.find_all("b"):
                                            for word in tokenize(tag.get_text(separator=" ")):
                                                if word not in stopwords:
                                                    tokens[word] = tokens[word] + 0.2
                                        for tag in soup.find_all("strong"):
                                            for word in tokenize(tag.get_text(separator=" ")):
                                                if word not in stopwords:
                                                    tokens[word] = tokens[word] + 0.2

                                        # print("******************************************************************")
                                        # print(tokens)

                                        for k, v in tokens.items():
                                            if k not in table.keys():
                                                p = Posting(n, v)
                                                table[k] = [(p.docid, p.tfidf)]
                                            else:
                                                p = Posting(n, v)
                                                table[k].append((p.docid, p.tfidf))
                                        if n % 5000 == 0:
                                            table_list = sorted(table.items())
                                            pickle.dump(table_list, open('disk/mergefile' + str(n) + '.pickle', 'wb'))

                                            table.clear()
                                        first = False;
                                    else:
                                        print("This file is similar")
                                else:
                                    print("URL invalid")
                            except:
                                print("Get response error")
                        else:
                            print("THIS URL HAS ALREADY BEEN FOUND")

        table_list = sorted(table.items())
        pickle.dump(table_list, open('disk/mergefile' + str(n) + '.pickle', 'wb'))
        table.clear()
        print("DONE")
        pickle.dump(docLength, open('docLengthFile.pickle', 'wb'))

    FINAL_INDEX = []

    diskfiles = os.listdir('disk')
    print(diskfiles)

    for picklefile in diskfiles:
        if str(picklefile)[-6:] == "pickle":
            print("****** testing " + str(picklefile))
            # print(len(FINAL_INDEX))
            # FINAL_INDEX = [('2007', [(99999, 2)]), ('30000', [(69, 1)])]
            final_i = 0
            second_i = 0
            # second_pickle_file = test_list
            # with open('disk/' + str(picklefile), 'rb') as fin:
            #    second_pickle_file = pickle.load(fin)
            second_pickle_file = pickle.load(open('disk/' + str(picklefile), 'rb'))
            print("_________________________________")
            while final_i < len(FINAL_INDEX) and second_i < len(second_pickle_file):
                # print(final_i)
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
    pickle.dump(d, open('urls.pickle', 'wb'))
    f = open("results.txt", "a")
    for thing in FINAL_INDEX:
        f.write("TOKEN: " + str(thing[0]) + "   POSTINGS: " + str(thing[1]))
        f.write("\n")
        f.write(
            "________________________________________________________________________________________________________________")
        f.write("\n")
    f.close()
    print("FINAL_INDEX = ")
    print(len(FINAL_INDEX))
    return FINAL_INDEX


def simhash(d):
    # resp = get_response(url)
    # if (resp == None):
    #     print("This url has an empty response: " + url)
    #     #failedlinks.append(url)
    #     return ((2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dict())

    vector = {}
    for i in d.keys():
        l = []
        hashnum = format(hash(i) % 32768, '015b')
        for j in hashnum:
            l.append(j)
        vector[i] = l
    final = []
    for i in range(15):
        add = 0
        for k, v in vector.items():
            if v[i] == '1':
                add += d[k]
            else:
                add -= d[k]
        final.append(add)

    ans = []
    for i in final:
        if i > 0:
            ans.append(1)
        else:
            ans.append(0)
    return tuple(ans)


if __name__ == '__main__':
    empty_dict = dict()
    # empty_dict = pickle.load(open(empty_dict, 'disk/disk5000.pickle', 'rb'))
    f = open("stopwords.txt")
    for line in f:
        stopwords.add(line.strip("\n"))
    f.close()
    print(stopwords)
    a = os.walk('DEV')
    result = build_index(a)
    print(result)
    # test([('2007', [(9, 2), (51, 2), (58, 1), (99, 3)]), ('2010', [(67, 1)]), ('2011', [(6, 1)])])

    # for k,v in result.items():
    #     print(k,v)

    # hi = [1,2,3]
    # pickle.dump(hi, open('gamestate.pickle', 'wb'))
    # diskstuff = pickle.load(open('gamestate.pickle', 'rb'))
    # print(diskstuff)
