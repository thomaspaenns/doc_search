import gzip
import sys
import os
import pathlib
from pathlib import Path
from turtle import rt
import pickle
import Helper




if not len(sys.argv) > 1:
    sys.exit("Enter Filepaths Please")
#retrieved from: https://stackoverflow.com/questions/14360389/getting-file-path-from-command-line-argument-in-python
dataFile = sys.argv[1] 
dataPath = Path(dataFile)

# retreived from: https://stackoverflow.com/questions/10566558/python-read-lines-from-compressed-text-files
with gzip.open(dataPath, mode="rt") as fileData: 
    document = []
    docNo = ""
    docDate = ""
    docId = 0
    headLine = ""
    inHeadLine = False
    docText = ""
    inText = False
    inGraphic = False
    docIndex = {}
    for line in fileData: #For each line in master file
        #Retrieved from Answer 864: https://stackoverflow.com/questions/3437059/does-python-have-a-string-contains-substring-method
        if line.find("<DOC>") != -1: #re-initialize to zero
            document = []
            headLine = ""
            docText = ""
        elif line.find("<DOCNO>") != -1: #Grab DOCNO and Headline
            docNo = line.replace("<DOCNO>", "")
            docNo = docNo.replace("</DOCNO>", "")
            docNo = docNo.strip()
            docDate = docNo[2:8]
        elif line.find("<DOCID>") != -1: #Grab DOCID
            docId = line.replace("<DOCID>", "")
            docId = docId.replace("</DOCID>", "")
            docId = docId.strip()
            docId = int(docId)          
        elif line.find("<HEADLINE>") != -1 or inHeadLine: #Parse HEADLINE
            inHeadLine = True
            headLine = headLine + line
            docText = docText + line
            if line.find("</HEADLINE>") != -1:
                headLine = headLine.replace("<HEADLINE>", "")
                headLine = headLine.replace("</HEADLINE>", "")
                headLine = headLine.replace("<P>", "")
                headLine = headLine.replace("</P>", "")
                headLine = headLine.replace("\n", "")
                inHeadLine = False
        elif line.find("<TEXT>") != -1 or inText:
            inText = True
            docText = docText + line
            if line.find("</TEXT>") != -1:
                inText = False
        elif line.find("<GRAPHIC>") != -1 or inGraphic:
            inGraphic = True
            docText = docText + line
            if line.find("</GRAPHIC>") != -1:
                inGraphic = False
        document.append(line)
        if line.find("</DOC>") != -1: #End of doc, save doc and move along
            #dateFile = targetFile + "\\" + docDate
            #datePath = Path(dateFile)
            #pathlib.Path(datePath).mkdir(parents=True, exist_ok=True) #create date folder of not already existing
            #tokens = Helper.tokenize(docText)
            #tokenIds = convertTokensToIds(tokens, lexicon)
            #wordCounts = Helper.countWords(tokenIds)
            #invIndex = Helper.addToPostings(wordCounts, docId, invIndex)
            #docMetaData = {"DOCNO":docNo, "DOCID":docId, "DATE":docDate, "HEADLINE":headLine, "LENGTH":len(tokens)}
            #Retrieved from https://www.w3schools.com/python/python_dictionaries_nested.asp
            #metaData.update({docNo:docMetaData}) 
            #idConvert.update({docId:docNo})
            #docFile = dateFile + "\\" + docNo + ".txt"
            #docPath = Path(docFile)
            #with open(docPath, mode = "wt") as newDoc:
                #newDoc.write("\n".join(document))
            docText = docText.replace("<GRAPHIC>","")
            docText = docText.replace("</GRAPHIC>","")
            docText = docText.replace("<TEXT>","")
            docText = docText.replace("</TEXT>","")
            docText = docText.replace("<HEADLINE>","")
            docText = docText.replace("</HEADLINE>","")
            docText = docText.replace("<P>","")
            docText = docText.replace("</P>","")
            docText = docText.replace("\n", " ")
            docIndex.update({docNo:docText})
            headLine = ""
    #Retrieved from: https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict-or-any-other-python-object 
    with open('docIndex.pickle', 'wb') as picklePath:
        pickle.dump(docIndex, picklePath)