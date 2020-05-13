import part1
import pickle

inverted_index = {}

def get_ID(query):
    if query in inverted_index:
        return inverted_index[query]
    return []



if __name__ == '__main__':
    inverted_index = dict(pickle.load(open('final_index.pickle', 'rb')))
    full_query = "cristina lopes"
    wordlist = full_query.split(" ")
    wordlist = [value for value in wordlist if value.lower() != "and"]
    id_list = []
    for word in wordlist:
        print(word)
        # id_list.append([k[0] for k in get_ID(word)])
        id_list.append(get_ID(word))
    print(len(id_list))



