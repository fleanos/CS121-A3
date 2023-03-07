from os import walk 
from os import path
import pickle
from TFIDF import calcIDF
import json

def findAllFiles(folder: str) -> set:
  return {path.join(root, file) for root, _, files in walk(folder, topdown=True) for file in files}

def splitFragIndexByChar(fragIndexPath):
  indexDict = dict()
  fragmentedIndex = pickle.load(open(fragIndexPath, "rb"))
  for word in fragmentedIndex.keys():
    firstChar = word[0]
    if firstChar in indexDict:
      if word in indexDict[firstChar]:
        indexDict[firstChar][word].update(fragmentedIndex[word])
      else:
        indexDict[firstChar][word] = fragmentedIndex[word]
    else:
      indexDict[firstChar] = {word:fragmentedIndex[word]}
  return indexDict


def tfidfSortPostings(indexPath, corpusLen):
  for i in findAllFiles(indexPath):
    charDict = pickle.load(open(i, "rb"))
    for word in charDict.keys():
      wordPosting = list(charDict[word])
      for index in range(len(wordPosting)):
        wordInfo = wordPosting[index]
        wordPosting[index] = (wordInfo[0], wordInfo[1] * calcIDF(len(wordPosting), corpusLen), wordInfo[2])
      charDict[word] = sorted(wordPosting, key = lambda x:x[1], reverse = True)
    pickle.dump(charDict, open(i, "wb"), pickle.HIGHEST_PROTOCOL)

def splitIndexToJson(folderPath):
  wordLineDic = dict()
  f = open("Index.json", "a")
  for i in findAllFiles(folderPath):
    print(i)
    charDict = pickle.load(open(i, "rb"))
    for word in charDict.keys():
      postingJson = json.dumps(charDict[word])
      wordLineDic[word] = f.tell()
      f.write(postingJson)
      f.write("\n")
  f.close()
  with open("wordSeekPos.json", "w") as f:
    json.dump(wordLineDic, f)

def combineIndexChar(folder, corpusLen):
  indexPaths = findAllFiles(folder)
  for i in indexPaths:
    indexDict = splitFragIndexByChar(i)

    for char in indexDict.keys():
      if path.exists(path.join("Char_Split_Index", char + ".txt")): charDict = pickle.load(open(path.join("Char_Split_Index", char + ".txt"), "rb"))
      else: charDict = {}

      for word in indexDict[char]:
        if word in charDict:
          charDict[word].update(indexDict[char][word])
        else:
          charDict[word] = indexDict[char][word]
    
      pickle.dump(charDict, open(path.join("Char_Split_Index", char + ".txt"), "wb"), pickle.HIGHEST_PROTOCOL)

  tfidfSortPostings("Char_Split_Index", corpusLen)
  splitIndexToJson("Char_Split_Index")