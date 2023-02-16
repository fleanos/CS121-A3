from parseDocs import *
from storeIndex import *
from tokenizer import *
from os import walk

"Main script combines the 3 file's functions - need to wait till everyone done"

def findAllFiles(folder : str) -> set:
  allFilePaths = set()
  for (root,dirs,files) in walk(folder, topdown=True):
    for i in files:
      allFilePaths.add(root + "/" + i)
  return allFilePaths

def buildIndex(folderPath):
  files = findAllFiles(folderPath)
  for i in files:
    wordList = getStrings(i)

if __name__ == "__main__":
  buildIndex("ANALYST")