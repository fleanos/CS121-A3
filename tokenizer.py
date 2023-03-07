"Recieves list of string words, tokeize all words, and count frequceny of all them, return set of tuples containing word and freq"
from collections import defaultdict
from nltk.stem import PorterStemmer
from TFIDF import calcTF

def tokenize(words: list, importantWords) -> set:
    ps = PorterStemmer()
    freqDict = defaultdict(int)
    importantWordsStemmed = set()
    for token in importantWords:
        token = token.replace("'", "")
        token = token.replace("`", "")
        token = ps.stem(token)
        if(len(token) > 0): importantWordsStemmed.add(token)

    for token in words:
        token = token.replace("'", "")
        token = token.replace("`", "")
        token = ps.stem(token)
        if(len(token) > 0): freqDict[token] += 1
    numTokens = sum(freqDict.values())
    return {(token, calcTF(token, freqDict, numTokens), token in importantWordsStemmed) for token in freqDict}