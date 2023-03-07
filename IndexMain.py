import multiprocessing
import pickle
import time
from os import mkdir, path

import numpy as np

from combineIndex import *
from parseDocs import *
from tokenizer import *


def compute(files, processNum):
  tokenDict = dict()
  for i in files:
    url, tokens, importantWords = getStrings(i)
    for token, tf, importantBool in tokenize(tokens, importantWords):
      if token in tokenDict: tokenDict[token].add((url, tf, importantBool))
      else: tokenDict[token] = {(url, tf, importantBool)}
  pickle.dump(tokenDict, open(path.join("Split_Index", "Index" + str(processNum) + ".txt"), "wb"), pickle.HIGHEST_PROTOCOL)
  print(f"Process: {processNum} - DONE")

def buildIndex(folderPath : str) -> None:
  allFilePaths = list(findAllFiles(folderPath))
  filePaths = np.array_split(allFilePaths, 6)

  if not path.exists("Split_Index"): mkdir("Split_Index")
  if not path.exists("Char_Split_Index"): mkdir("Char_Split_Index")

  #splits the creation of index into 6 different parts - i.e. off loading the inverted index from main mem to disk 6 times
  """
  for i in range(6):
    compute(filePaths[i], str(i))
  """

  #using multiprocessing for speed when testing, use for loop above when properly off loading index for assignment req.
  p1 = multiprocessing.Process(target=compute, args=(filePaths[0], "1", ))
  p2 = multiprocessing.Process(target=compute, args=(filePaths[1], "2", ))
  p3 = multiprocessing.Process(target=compute, args=(filePaths[2], "3", ))
  p4 = multiprocessing.Process(target=compute, args=(filePaths[3], "4", ))
  p5 = multiprocessing.Process(target=compute, args=(filePaths[4], "5", ))
  p6 = multiprocessing.Process(target=compute, args=(filePaths[5], "6", ))
  
  p1.start()
  p2.start()
  p3.start()
  p4.start()
  p5.start()
  p6.start()

  p1.join()
  p2.join()
  p3.join()
  p4.join()
  p5.join()
  p6.join()
 
  combineIndexChar("Split_Index", len(allFilePaths))

if __name__ == "__main__":
  start = time.time()
  buildIndex("developer")
  print("Time:", time.time() - start)
  print("Done")