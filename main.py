from parseDocs import *
from storeIndex import *
from tokenizer import *
from os import walk
from os import path
import numpy as np
import multiprocessing

def findAllFiles(folder: str) -> set:
  return {path.join(root, file) for root, _, files in walk(folder, topdown=True) for file in files}

def compute(files, threadNum):
  for i in files:
    for token, freq in tokenize(getStrings(i)):
      storeData(i, token, freq, threadNum)

def buildIndex(folderPath : str) -> None:
 
  filePaths = np.array_split(list(findAllFiles(folderPath)), 6)

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

if __name__ == "__main__":
  buildIndex("ANALYST")
  print("Done")
