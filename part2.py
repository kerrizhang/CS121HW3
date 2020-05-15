import part1
import pickle
import math

inverted_index = {}
stopwords = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours     ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"}

def get_ID(query):
    if query in inverted_index:
        return inverted_index[query]
    return []

def tfidf(id_list):
    d = {}
    for tup in id_list:
        d[tup[0]] = (1+math.log10(tup[1])) * math.log10(55393/len(id_list))
    return d


if __name__ == '__main__':
    inverted_index = dict(pickle.load(open('final_index.pickle', 'rb')))
    di = pickle.load(open('urls.pickle', 'rb'))
    print(di)
    full_query = "cristina lopes"
    wordlist = full_query.split(" ")
    wordlist = [value for value in wordlist if value.lower() != "and" and value.lower() not in stopwords]
    id_list = []
    intersection = set()
    newl = []
    for word in wordlist:
        docids = set()
        print(word)
        '''
        l = get_ID(word)
        if len(l) != 0:
            for tup in l:
        else:
            intersection = get_ID(word)
        '''

        #print(tfidf(get_ID(word), 55395))
        #id_list.append([k[0] for k in get_ID(word)])
        l = get_ID(word)
        id_list.append(l)
        for i in l:
            docids.add(i[0])
        if len(intersection) == 0:
            intersection = docids
        else:
            intersection = docids.intersection(intersection)
        print(docids)
    print(intersection)
    for id in intersection:
        counter = 0
        for l in id_list:
            for tup in l:
                if id == tup[0]:
                    counter += tup[1]
        newl.append((id, counter))
    print("newl:", newl)
    d = tfidf(newl)
    li = sorted(d.items(), key=lambda x:x[1], reverse = True)
    #print(di)
    for thing in li[:5]:
        print(thing[0])
        print(di[thing[0]])




        
        
    
    

    #print(id_list)
    




