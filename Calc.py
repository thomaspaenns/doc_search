#Program to generate number of words and number of non-zero instances of terms in documents
#Also used to calculate average document length in collection
import pickle

with open("lexicon.pickle", "rb") as lex:
    lexicon = pickle.load(lex) 
    print(len(lexicon))


with open("invIndex.pickle", "rb") as index:
    invIndex = pickle.load(index) 
    totalLen = 0
    for tokenID in invIndex:
        postings = invIndex[tokenID]
        totalLen += len(postings)
    print(totalLen)

with open("metaData.pickle", "rb") as md:
    metaData = pickle.load(md)
    totalLen = 0
    count = 0
    for docno in metaData:
        docLen = metaData[docno]["LENGTH"]
        totalLen += docLen
        count += 1
    avgLen = float(totalLen)/count
    #avgLen = float(totalLen)/131896.0

    print(avgLen)


