import math

def calcTF(token, freqDict, numOfTokens):
    return freqDict[token] / numOfTokens

def calcIDF(numToken, corpusLen):
    return math.log(corpusLen / numToken + 1)