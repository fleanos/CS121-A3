import math

# Calculate the term frequency of the given token
def calcTF(token, freqDict, numOfTokens):
    return freqDict[token] / numOfTokens

# Calculate the inverse document frequency of the given number of tokens and corpus length
def calcIDF(numToken, corpusLen):
    return math.log(corpusLen / numToken + 1)