import sys
import pathlib
from pathlib import Path
import pickle
import os
from turtle import rt
import Helper
import math
import heapq

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
metaData = {}
with open('invIndex.pickle', 'rb') as picklePath4:
    invIndex = pickle.load(picklePath4)
with open('lexicon.pickle', 'rb') as picklePath3:
    lexicon = pickle.load(picklePath3)
with open('idConvert.pickle', 'rb') as picklePath2:
    idConvert = pickle.load(picklePath2)
with open('metaData.pickle', 'rb') as picklePath1:
    metaData = pickle.load(picklePath1)

k1 = 1.2
b = 0.75
k2 = 7
N = 131896
avgDl = 534.4707345181051
with open(queries, 'rt') as qFile:
    res = ""
    for line in qFile:
        queryId = line[0:3]
        query = line.replace(queryId, '')
        tokens = Helper.tokenize(query)
        tokenIds = convertTokensToIds(tokens, lexicon)
        bm25Scores = {}
        for tokenId in tokenIds:
            postings = invIndex[tokenId]
            ni = len(postings)
            for docId in postings:
                fi = postings[docId]
                qfi = 1
                docno = idConvert[docId]
                dl = float(metaData[docno]["LENGTH"])
                K = k1*((1-b)+b*(dl/avgDl))
                partialScore = (((k1+1)*fi)/(K+fi))*(((k2+1)*qfi)/(k2+qfi))*math.log((N-ni+0.5)/(ni+0.5))
                if docId in bm25Scores.keys():
                    score = bm25Scores[docId]
                    score = score + partialScore
                    bm25Scores.update({docId:score})
                else:
                    bm25Scores.update({docId:partialScore})
        sortedScores = []
        for docId in bm25Scores.keys():
            sortedScores.append((bm25Scores[docId],str(docId)))
            #heapq.heappush(sortedScores, (bm25Scores[docId],str(docId)))
        sortedScores.sort()
        i = len(sortedScores) - 1
        stop = i - 1000
        rank = 1
        while i > stop and i >= 0:
            result = int(sortedScores[i][1])
            res = res + queryId + " Q0 " + idConvert[result] + " " + str(rank) + " " + str(sortedScores[i][0]) + " tennsAND" + "\n"
            i = i - 1
            rank = rank + 1
    with open(outputName, 'wt') as output:
        output.write(res)


