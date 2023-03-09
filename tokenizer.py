from collections import defaultdict
from nltk.stem import PorterStemmer
from TFIDF import calcTF

"""
tokenize() function takes two arguments: a list of words and a set of important words. 
It then returns a set of tuples, where each tuple contains a token, its term frequency (TF), 
and a boolean indicating whether the token is one of the important words. 
"""
def tokenize(words: list, importantWords) -> set:
    # Create a PorterStemmer object
    ps = PorterStemmer()

    # Create an empty dictionary to store the frequency of each token
    freqDict = defaultdict(int)

    # Create an empty set to store the stemmed versions of the important words
    importantWordsStemmed = set()

    # Loop through each important word, stem it, and add it to the set of stemmed important words
    for token in importantWords:
        token = token.replace("'", "")
        token = token.replace("`", "")
        token = ps.stem(token)
        if(len(token) > 0): importantWordsStemmed.add(token)

    # Loop through each word, stem it, and add it to the frequency dictionary
    for token in words:
        token = token.replace("'", "")
        token = token.replace("`", "")
        token = ps.stem(token)
        if(len(token) > 0): freqDict[token] += 1
    
    # Calculate the total number of tokens
    numTokens = sum(freqDict.values())

    # Create a set of tuples containing the token, its TF, and a boolean indicating whether it is an important word
    return {(token, calcTF(token, freqDict, numTokens), token in importantWordsStemmed) for token in freqDict}