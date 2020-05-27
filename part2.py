import part1
import pickle
import math
import sys
from flask import Flask, render_template, request

app = Flask(__name__)

inverted_index = dict(pickle.load(open('final_index.pickle', 'rb')))
docid_urls = pickle.load(open('urls.pickle', 'rb'))

stopwords = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
             "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
             "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
             "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
             "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
             "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
             "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
             "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
             "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
             "yourselves"}


@app.route('/')
def index():
    return render_template('search.html')


def get_ID(query):
    if query in inverted_index:
        return inverted_index[query]
    return []


def tfidf(id_list):
    #id_list = documents that contain the token
    d = {}
    for tup in id_list:
        d[tup[0]] = (1 + math.log10(tup[1])) * math.log10(55393 / len(id_list))
    return d


def query_cos(query):
    term_freq = dict()
    #term_freq = {term in query: tf*idf}
    #term list = number of docs the term shows up in (length of posting list)
    for token in query:
        print(token)
        if token in term_freq:
            term_freq[token] += 1
        else:
            term_freq[token] = 1
    for tok, tf in term_freq.items():
        idf = math.log10(55393 /len(inverted_index[tok]))
        term_freq[tok] = tf * idf
    return normalize(term_freq)


def normalize(term_freq):
    qnum_sum = 0
    for token, tfidf in term_freq.items():
        qnum_sum += pow(tfidf, 2)
    normalize_dict = dict()
    for token, tfidf in term_freq.items():
        if qnum_sum != 0:
            normalize_dict[token] = tfidf / math.sqrt(qnum_sum)
    return normalize_dict


def doc_tfidf(intersection, query):
    doc_product = {}
    # doc_product = {docID: dotproduct}
    # print("Doc intersection: ", intersection)
    query_words = query
    print("intersection: ")
    print(intersection)
    # For each of the docid's in the intersection
    for docid in intersection:
        query_word_dict = {}
        # query_word_dict = {query_word: doc freq}
        for word in query_words:
                postings = inverted_index[word]
                for tup in postings:
                    if tup[0] == docid:
                        #FIX : replace key
                        query_word_dict[word] = (1 + math.log10(tup[1]))

        #TOOK OUT DOCUMENT DICT NORMALIZATION
        doc_norm_dict = query_word_dict#normalize(query_word_dict)
        # {query_word = doc_norm_freq}
        query_norm_dict = query_cos(query)
        print(docid_urls[docid])
        print("doc norm dict: ")
        print(doc_norm_dict)
        # {query_word = query_norm_freq}
        sorted_doc_norm = sorted(doc_norm_dict.items())
        sorted_query_norm = sorted(query_norm_dict.items())
        # sorted_doc_norm = [(term, tfidf_norm), ..]
        sum = 0
        if len(sorted_doc_norm) == len(sorted_query_norm):
            for i in range(len(sorted_doc_norm)):
                sum += (sorted_query_norm[i][1] * sorted_doc_norm[i][1])
        print("Sum for {}: {}".format(docid, sum))
        doc_product[docid] = sum
    #print("lol 20 results pls??")
    #print(doc_product[22576])
    return doc_product


@app.route('/', methods=['POST'])
def printvalue():
    name = request.form['query']

    #return "Search results for: " + name

    full_query = str(name)

    # wordlist = sys.argv[1:]
    # full_query = "cristina lopes"
    wordlist = full_query.split(" ")
    wordlist = [value.lower() for value in wordlist if value.lower() != "and" and value.lower() not in stopwords]
    # wordlist = [value.lower() for value in wordlist]
    #print("wordlist: ", wordlist)
    id_list = []
    intersection = set()
    newl = []
    for word in wordlist:
        docids = set()

        l = get_ID(word)
        # print(l)
        id_list.append(l)
        for i in l:
            docids.add(i[0])
        if len(intersection) == 0:
            # print(docids)
            intersection = docids
        else:
            intersection = docids.intersection(intersection)

    top_urls = doc_tfidf(list(intersection), wordlist)
    # top_urls = {docIDs, cosine_similarity}
    sorted_urls = sorted(top_urls.items(), key=lambda x: x[1], reverse=True)
    # sorted_url [(docIDs, cosine_similarity), ...]
    for tup in sorted_urls[:5]:
        print(docid_urls[tup[0]])

    n_1 = docid_urls[sorted_urls[0][0]]
    n_2 = docid_urls[sorted_urls[1][0]]
    n_3 = docid_urls[sorted_urls[2][0]]
    n_4 = docid_urls[sorted_urls[3][0]]
    n_5 = docid_urls[sorted_urls[4][0]]

    return render_template('results.html', n=name, n1=n_1, n2=n_2, n3=n_3, n4=n_4, n5=n_5)
    #return render_template('results.html', n=name, n1=1, n2=2, n3=3, n4=4, n5=5)




if __name__ == '__main__':
    app.run(debug=True)
    #print("doc_tfidf")
    #doc_tfidf([22576], "cristina lopes")
    #print(query_cos("cristina lopes"))

    
    var = True
    while var:
        full_query = input("Enter your query: ")
        if full_query == "":
            break
        # wordlist = sys.argv[1:]
        # full_query = "cristina lopes"
        wordlist = full_query.split(" ")
        wordlist = [value.lower() for value in wordlist if value.lower() != "and" and value.lower() not in stopwords]
        # wordlist = [value.lower() for value in wordlist]
        print("wordlist: ", wordlist)
        id_list = []
        intersection = set()
        newl = []
        for word in wordlist:
            docids = set()

            l = get_ID(word)
            # print(l)
            id_list.append(l)
            for i in l:
                docids.add(i[0])
            if len(intersection) == 0:
                # print(docids)
                intersection = docids
            else:
                intersection = docids.intersection(intersection)

        top_urls = doc_tfidf(list(intersection), wordlist)
        # top_urls = {docIDs, cosine_similarity}
        sorted_urls = sorted(top_urls.items(), key=lambda x: x[1], reverse=True)
        # sorted_url [(docIDs, cosine_similarity), ...]
        for tup in sorted_urls[:5]:
            print(docid_urls[tup[0]])

        for id in intersection:
            counter = 0
            for l in id_list:
                for tup in l:
                    if id == tup[0]:
                        counter += tup[1]
            newl.append((id, counter))
        #print("newl:", newl)
        # newl = [(docID, tf)]
        d = tfidf(newl)
        li = sorted(d.items(), key=lambda x: x[1], reverse=True)

        for thing in li[:5]:
            print("intersection urls for comparison: ")
            print(thing[0])
            print(docid_urls[thing[0]])

    #print(id_list)
    






