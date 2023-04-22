import sys
import pathlib
from pathlib import Path
import pickle
import os
from turtle import rt
import Helper

def numToStringMonth(monthNum): #Convert numerical month to string
    if monthNum == "01":
        return "January"
    elif monthNum == "02":
        return "February"
    elif monthNum == "03":
        return "March"
    elif monthNum == "04":
        return "April"
    elif monthNum == "05":
        return "May"
    elif monthNum == "06":
        return "June"
    elif monthNum == "07":
        return "July"
    elif monthNum == "08":
        return "August"
    elif monthNum == "09":
        return "September"
    elif monthNum == "10":
        return "October"
    elif monthNum == "11":
        return "November"
    elif monthNum == "12":
        return "December"

if not len(sys.argv) > 3: #too few arguments
    sys.exit("Enter correct arguments please. The correct arguments are: *FilePath to the documents* \"docno\"/\"id\" *DOCNO*/*ID*")
filePath = sys.argv[1]
docInput = sys.argv[2] 
idNo = sys.argv[3]
docInputUpper = docInput.upper()
docNo = ""
docMetaData = {}
#Retrieved from: https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict-or-any-other-python-object 
with open("idConvert.pickle", "rb") as convert:
    idConvert = pickle.load(convert)  
    if docInputUpper.find("DOCNO") != -1:
        docNo = idNo
    elif docInputUpper.find("ID") != -1:
        idNo = int(idNo)
        if not idNo in idConvert.keys():
            sys.exit("Enter a valid ID")
        docNo = idConvert[idNo]
    else:
        sys.exit("Enter either a DOCNO or an id")

with open("metaData.pickle", "rb") as mData:
    metaData = pickle.load(mData)
    if not docNo in metaData.keys():
        sys.exit("Enter a valid DOCNO")
    docMetaData = metaData[docNo]
    docDate = docMetaData["DATE"]
docFile = filePath + "\\" + docDate + "\\" + docNo + ".txt" #create filePath for document
docPath = Path(docFile)
if not os.path.exists(docPath):
    sys.exit("File does not exist")
print("docno: " + docNo)
print("internal id: " + str(docMetaData["DOCID"]))
mString = docDate[0:2]
dString = docDate[2:4]
yString = docDate[4:6]
print("date: " + numToStringMonth(mString) + " " + str(int(dString)) +", 19" + yString)#DATE
print("headline: " + docMetaData["HEADLINE"])
print("raw document:")
with open(docPath) as doc: #Print document to console
    for line in doc:
        docLine = line.replace("\n", "")
        if len(docLine) > 0:
            print(docLine)


    
