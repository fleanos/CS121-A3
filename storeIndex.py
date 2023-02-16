import pickle
from os import path

def loadData(firstChar : str) -> dict:
  if firstChar.isalnum():
    if not path.exists(firstChar + ".txt"): tokens = dict()
    else: tokens = pickle.load(open(firstChar + ".txt", "rb"))

  else:
    if not path.exists("NonAlnum.txt"): tokens = dict()
    else: tokens = pickle.load(open("NonAlnum.txt", "rb"))

  return tokens

def dumpData(tokens : dict, firstChar : str) -> None:
  if firstChar.isalnum():
    pickle.dump(tokens, open(firstChar + ".txt", "wb"), pickle.HIGHEST_PROTOCOL)
  else:
    pickle.dump(tokens, open("NonAlnum.txt", "wb"),pickle.HIGHEST_PROTOCOL)

  
def storeData(page : str, word : str, freq : int) -> None:
  if page == "": return
  if word == "": return
  if freq == 0: return

  storedTokens = loadData(word[0])

  if word in storedTokens: storedTokens[word].add((page, freq))
  else: storedTokens[word] = {(page, freq)}

  dumpData(storedTokens, word[0]) 