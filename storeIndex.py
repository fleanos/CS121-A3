import pickle
from os import path

def loadData(firstLetter : str) -> dict:
  if not path.exists(firstLetter + ".txt"): tokens = dict()
  else: tokens = pickle.load(open(firstLetter + ".txt", "rb"))

  return tokens

def dumpData(tokens : dict, firstLetter : str) -> None:
  pickle.dump(tokens, open(firstLetter + ".txt", "wb"), pickle.HIGHEST_PROTOCOL)
  
def storeData(page : str, word : str, freq : int) -> None:
  if word == "": return
  if freq == "": return
  if page == "": return

  storedTokens = loadData(word[0])

  storedTokens[word] = (page, freq)

  dumpData(storedTokens, word[0]) 