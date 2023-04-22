import sys
import os
import pathlib
from pathlib import Path
from turtle import rt
import math
import pickle
import csv

if not len(sys.argv) > 2: #too few arguments
    sys.exit("Enter the name of the qrels file and the name of the results file please. \n Note that all the results files must be in a folder named \"results-files\" in the root directory of the project")
qrelsFile = sys.argv[1]
resultsFile = sys.argv[2]
#NEXT TWO LINES CHANGED FROM HW3
resultName = resultsFile.replace(".txt", "")
#resultName = resultsFile.replace(".results", "")
resultsFile = resultsFile
#resultsFile = "results-files/" + resultsFile
resultsPath = Path(resultsFile)

queriesDef = [401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 
    417, 418, 419, 420, 421, 422, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 
    435, 436, 438, 439, 440, 441, 442, 443, 445, 446, 448, 449, 450]

#Read qrels and put data in nested dictionary
qrels = {}
with open(qrelsFile, 'rt') as qrelsF:
    for line in qrelsF:
        queryId = int(line[0:3])
        docno = line[6:19]
        judgement = int(line[20])
        if queryId in qrels.keys():
            rels = qrels[queryId]
            rels.update({docno:judgement})
            qrels.update({queryId:rels})
        else:
            rel = {docno: judgement}
            qrels.update({queryId:rel})

def getJudgement(docno, queryId): #return judgement given docno and query from qrels
    rels = qrels[queryId]
    if docno in rels.keys():
        return rels[docno]
    else:
        return 0

results = {}
with open(resultsPath, 'rt') as resultsF: #array inside a dictionary inside a dictionary {QueryId:{rank:[docno,judgement]}}
    for line in resultsF:
        line = line.split()
        if (not len(line) == 6) or (not line[0].startswith("4")) or (not line[2].isupper()) or (line[2].startswith("[")):
            sys.exit("Use correctly formatted results file please")
        queryId = int(line[0])
        docno = line[2]
        rank = int(line[3])
        if queryId in results.keys():
            query = results[queryId]
            query.update({rank:[docno,getJudgement(docno,queryId)]})
            results.update({queryId:query})
        else:
            results.update({queryId:{rank:[docno,getJudgement(docno,queryId)]}})

#Calculate Average Precisions
averagePrecision = {}
average10Precision = {}
for query in results:
    resultCount = 0.0
    relevantResultCount = 0.0
    averagePrecisionAtN = 0.0
    result = results[query]
    rel = qrels[query] #New
    totalRelevantDocs = 0 #New
    tRD10 = 10.0 #New
    for docno in rel: #New
        if rel[docno] > 0: #New
            totalRelevantDocs = totalRelevantDocs+ 1 #New
    for rank in result:
        resultCount = resultCount + 1
        info = result[rank]
        relevantResultCount = relevantResultCount + info[1]
        averagePrecisionAtN = averagePrecisionAtN + info[1]*(float(relevantResultCount)/resultCount)
        if resultCount == 1000 or resultCount == len(result): #ADDED OR STATEMENT TO FIX MISSING 403
            averagePrecision.update({query:(averagePrecisionAtN / totalRelevantDocs)})
        if resultCount == 10 or (resultCount == len(result) and resultCount <= 10): #ADDED OR STATEMENT TO FIX MISSING 410:
            #average10Precision.update({query:(relevantResultCount / resultCount)}) New
            average10Precision.update({query:(relevantResultCount / tRD10)}) #New
#print("averagePrecision")
#print(averagePrecision)
#print("average10Precision")
#print(average10Precision)

def DCG(k, qResults):
    DCG = 0
    i = 1
    for rank in qResults:
        if i <= k:
            info = qResults[rank]
            gain =  info[1]
            discount = math.log2(i+1)
            DCG = DCG + (gain/discount) #ADD SOME SHIT
            i = i + 1
    return DCG

def IDCG(k, qrels, query):
    rels = qrels[query]
    IDCG = 0
    i = 1
    for docno in rels:
        gain = rels[docno]
        if i <= k and gain > 0:
            gain = rels[docno]
            discount = math.log2(i+1)
            IDCG = IDCG + (gain/discount)
            i = i + 1
    return IDCG

#Call DCG and IDCG to calculate nDCG at 10 and 1000
nDCG10 = {}
nDCG1000 = {}
for query in results:
    qResults = results[query]
    DCG10 = DCG(10, qResults)
    IDCG10 = IDCG(10, qrels, query)
    DCG1000 = DCG(1000, qResults)
    IDCG1000 = IDCG(1000, qrels, query)
    nDCG10.update({query:(DCG10/IDCG10)})
    nDCG1000.update({query:(DCG1000/IDCG1000)})

#print("nDCG10")
#print(nDCG10)
#print("nDCG1000")
#print(nDCG1000)

#Get document length/metaData
metaData = {}
with open("metaData.pickle", "rb") as mData:
    metaData = pickle.load(mData)

#Calculated based on equation in campuswire question 
timeBiasedGain = {}
for query in results:
    qResults = results[query]
    TBG = 0.0
    Tk = 0.0
    for rank in qResults:
        info = qResults[rank]
        PC1R = 0.0 #Probability of clicking
        if info[1] > 0:
            PC1R = 0.64
        else:
            PC1R = 0.39
        if info[0] in metaData.keys(): #if document is not in metaData
            length = metaData[info[0]]["LENGTH"]
        else:
            length = 0.0
        Tk += 4.4 + (0.018*float(length) + 7.8)*PC1R #Maybe remove plus equals
        TBG = TBG + (info[1]*0.4928*math.exp((-Tk)*(math.log(2)/224)))
    timeBiasedGain.update({query:TBG})
#print("timeBiasedGain")
#print(timeBiasedGain)

folderPath = Path("measures-files")
pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
measuresFile = "measures-files/" + resultName + "-measures.txt"
measuresPath = Path(measuresFile)
with open(measuresPath, mode = "wt") as targetRead:
    measures = ""
    for  query in queriesDef:
        if query in averagePrecision.keys(): #for queries that are not in results file
            measures = measures + "AP    " + str(query) + "    " + str(averagePrecision[query]) + "\n"
        else:
            measures = measures + "AP    " + str(query) + "    " + "0.0" + "\n"
    for query in queriesDef:
        if query in average10Precision.keys():
            measures = measures + "P@10    " + str(query) + "    " + str(average10Precision[query]) + "\n"
        else:
            measures = measures + "P@10    " + str(query) + "    " + "0.0" + "\n"
    for query in queriesDef:
        if query in nDCG10.keys():
            measures = measures + "nDCG@10    " + str(query) + "    " + str(nDCG10[query]) + "\n"
        else:
            measures = measures + "nDCG@10    " + str(query) + "    " + "0.0" + "\n"
    for query in queriesDef:
        if query in nDCG1000.keys():
            measures = measures + "nDCG@1000    " + str(query) + "    " + str(nDCG1000[query]) + "\n"
        else:
            measures = measures + "nDCG@1000    " + str(query) + "    " + "0.0" + "\n"
    for query in queriesDef:
        if query in timeBiasedGain.keys():
            measures = measures + "TBG    " + str(query) + "    " + str(timeBiasedGain[query]) + "\n"
        else:
            measures = measures + "TBG    " + str(query) + "    " + "0.0" + "\n"
    targetRead.write(measures)
measuresCSV = "measures-files/" + resultName + "-measures.csv"
measuresCSVPath = Path(measuresCSV) 
#write same data to .csv for analysis
with open(measuresCSVPath, mode = "w", newline='') as targetCSV:
    writer = csv.writer(targetCSV)
    for query in queriesDef:
        row = []
        row.append(query)
        if query in averagePrecision.keys():
            row.append(averagePrecision[query])
            row.append(average10Precision[query])
            row.append(nDCG10[query])
            row.append(nDCG1000[query])
            row.append(timeBiasedGain[query])
        else:
            row.append(0.0)
            row.append(0.0)
            row.append(0.0)
            row.append(0.0)
            row.append(0.0)  
        writer.writerow(row)