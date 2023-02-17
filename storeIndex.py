import pickle
from os import path
import shelve

def loadData(firstChar : str, threadNum) -> dict:
  if firstChar.isalnum():
    if not path.exists("Index" + threadNum + "\\" + firstChar + ".txt"): tokens = dict()
    else: tokens = pickle.load(open("Index" + threadNum + "\\" + firstChar + ".txt", "rb"))

  else:
    if not path.exists("Index" + threadNum + "\\NonAlnum.txt"): tokens = dict()
    else: tokens = pickle.load(open("Index" + threadNum + "\\NonAlnum.txt", "rb"))

  return tokens

def dumpData(tokens : dict, firstChar : str, threadNum) -> None:
  if firstChar.isalnum():
    pickle.dump(tokens, open("Index" + threadNum + "\\" + firstChar + ".txt", "wb"), pickle.HIGHEST_PROTOCOL)
  else:
    pickle.dump(tokens, open("Index" + threadNum + "\\NonAlnum.txt", "wb"),pickle.HIGHEST_PROTOCOL)

  
def storeData(page : str, word : str, freq : int, threadNum : str) -> None:
  if page == "": return
  if word == "": return
  if freq == 0: return

  storedTokens = loadData(word[0], threadNum)

  if word in storedTokens: storedTokens[word].add((page, freq))
  else: storedTokens[word] = {(page, freq)}

  dumpData(storedTokens, word[0], threadNum) 

def storeDataShelve(page : str, word : str, freq : int) -> None:
  with shelve.open("data") as index:
    if word in index:
      index[word].add((page, freq))
    else:
      index[word] = {(page, freq)}