#Helper methods utilized in multiple files
import re
import nltk

def tokenize(docText):
    docText = docText.replace("<GRAPHIC>","")
    docText = docText.replace("</GRAPHIC>","")
    docText = docText.replace("<TEXT>","")
    docText = docText.replace("</TEXT>","")
    docText = docText.replace("<HEADLINE>","")
    docText = docText.replace("</HEADLINE>","")
    docText = docText.replace("<P>","")
    docText = docText.replace("</P>","")
    #docText = docText.replace("\n","")
    docText = docText.lower()
    tokens = re.split("\W+", docText)
    #RETRIEVED FROM: https://www.nltk.org/api/nltk.stem.porter.html
    stemmer = nltk.PorterStemmer(mode='MARTIN_EXTENSIONS') #COMMENT OUT TO REMOVE STEMMING
    if tokens[0] == "":
        tokens.pop(0)
    if len(tokens) > 0 and tokens[len(tokens) - 1] == "":
        tokens.pop(len(tokens)-1)
    #RETRIEVED FROM: https://www.nltk.org/howto/stem.html
    tokens = [stemmer.stem(token) for token in tokens] #COMMENT OUT TO REMOVE STEMMING
    return tokens

def countWords(tokenIds):
    wordCounts = {}
    for tokenId in tokenIds:
        if tokenId in wordCounts:
            wordCounts[tokenId] += 1
        else:
            wordCounts[tokenId] = 1
    return wordCounts

def addToPostings(wordCounts, docId, invIndex):
    for tokenId in wordCounts:
        count = wordCounts[tokenId]
        postings = {}
        if tokenId in invIndex:
            postings = invIndex[tokenId]
            postings.update({docId:count})
        else:
            postings = {docId:count}
        invIndex.update({tokenId:postings})
    return invIndex


