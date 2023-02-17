"Recieves list of string words, tokeize all words, and count frequceny of all them, return set of tuples containing word and freq"

from collections import defaultdict

def tokenize(words: list) -> set: #simple tokenizer for now
    freqDict = defaultdict(int)
    for token in words:
        freqDict[token] += 1

    return {(token, freqDict[token]) for token in freqDict}