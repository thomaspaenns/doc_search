import sys
import pathlib
from pathlib import Path
import pickle
import os
from turtle import rt
import Helper

def convertTokensToIds(tokens, lexicon):
    tokenIds = []
    for token in tokens:
        if token in lexicon:
            tokenIds.append(lexicon[token])
    return tokenIds

if not len(sys.argv) > 3: #too few arguments
    sys.exit("Enter correct arguments please")
fPath = sys.argv[1]
queries = sys.argv[2] 
outputName = sys.argv[3]

invIndex = {}
lexicon = {}
idConvert = {}
with open('invIndex.pickle', 'rb') as picklePath4:
    invIndex = pickle.load(picklePath4)
with open('lexicon.pickle', 'rb') as picklePath3:
    lexicon = pickle.load(picklePath3)
with open('idConvert.pickle', 'rb') as picklePath2:
    idConvert = pickle.load(picklePath2)


#filePath = Path(fPath)
with open(queries, 'rt') as qFile:
    res = ""
    for line in qFile:
        queryId = line[0:3]
        query = line.replace(queryId, '')
        tokens = Helper.tokenize(query)
        tokenIds = convertTokensToIds(tokens, lexicon)
        docCount = {}
        for tokenId in tokenIds:
            i = 1
            if tokenId in invIndex:
                postings = invIndex[tokenId]
                for docId in postings:
                    if docId in docCount:
                        docCount[docId] = docCount[docId] + 1
                    else:
                        docCount[docId] = 1
        resultSet = []
        for docId in docCount:
            if docCount[docId] == len(tokenIds):
                resultSet.append(docId)
        #resultSet = resultSet[0:10] REMOVED THIS SO THAT ALL DOCS ARE OUTPUTTED
        rank = 1
        for result in resultSet:
            res = res + queryId + " Q0 " + idConvert[result] + " " + str(rank) + " " + str(rank) + " tennsAND" + "\n"
            rank = rank + 1
        with open(outputName, 'wt') as output:
            output.write(res)

