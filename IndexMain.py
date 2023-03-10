import multiprocessing
import pickle
import time
from os import mkdir, path

import numpy as np

from combineIndex import *
from parseDocs import *
from tokenizer import *

"""
compute() function processes a list of files to create an inverted index, 
which maps terms to the documents in which they appear. It does this by first 
initializing an empty dictionary tokenDict, and then looping through each file 
in the given files list. For each file, it gets the URL, tokens, and important words 
using the getStrings() function, tokenizes the tokens and important words using the 
tokenize() function, and adds them to the tokenDict dictionary. Finally, it saves the 
tokenDict dictionary to a file using the pickle module
"""
def compute(files, processNum):
  # Create an empty dictionary to store tokens and their associated information
  tokenDict = dict()

  # Loop through each file in the given list of files
  for i in files:
    # Get the URL, tokens, and important words for the current file
    url, tokens, importantWords = getStrings(i)

    # Tokenize the tokens and important words, and add them to the token dictionary
    for token, tf, importantBool in tokenize(tokens, importantWords):
      if token in tokenDict: tokenDict[token].add((url, tf, importantBool))
      else: tokenDict[token] = {(url, tf, importantBool)}
  
  # Save the token dictionary to a file using pickle
  pickle.dump(tokenDict, open(path.join("Split_Index", "Index" + str(processNum) + ".txt"), "wb"), pickle.HIGHEST_PROTOCOL)

  print(f"Process: {processNum} - DONE")

"""
buildIndex() function builds an inverted index for all files in a given folder by first splitting the file paths into 6 parts 
and using multiprocessing to compute the inverted index for each part separately, then combining the resulting fragmented indexes 
by character, sorting the postings by TF-IDF score, and outputting the index as a JSON file.
"""
def buildIndex(folderPath : str) -> None:
  allFilePaths = list(findAllFiles(folderPath))

  # Splits all the paths into 6 different portions e.g. allow for off loading from main memory 6 different times or allow for multiprocessing
  filePaths = np.array_split(allFilePaths, 6)

  # Creates Folders to store the parital indexes
  if not path.exists("Split_Index"): mkdir("Split_Index")
  if not path.exists("Char_Split_Index"): mkdir("Char_Split_Index")

  # Splits the creation of index into 6 different parts - i.e. off loading the inverted index from main mem to disk 6 times
  """
  for i in range(6):
    compute(filePaths[i], str(i))
  """

  # Using multiprocessing for speed when testing, use for loop above when properly off loading index for assignment req.
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
  
  # CombineIndexChar() function is called to merage all the index files in Split_Index
  combineIndexChar("Split_Index", len(allFilePaths))

if __name__ == "__main__":
  start = time.time()
  buildIndex("developer")
  print("Time:", time.time() - start)
  print("Done")