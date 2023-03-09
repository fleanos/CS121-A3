from os import walk 
from os import path
import pickle
from TFIDF import calcIDF
import json

"""
findAllFiles() takes in a folder path and returns a set of all the file paths inside that folder.
"""
def findAllFiles(folder: str) -> set:
  return {path.join(root, file) for root, _, files in walk(folder, topdown=True) for file in files}

"""
splitFragIndexByChar() takes in a fragmented index file path, loads the fragmented index, 
and splits it into multiple dictionaries that are keyed by the first character of the word. 
It returns a dictionary where the keys are the first character of the words and the values 
are the inverted index for all the words that start with that character.
"""
def splitFragIndexByChar(fragIndexPath):
  indexDict = dict()

  # Load the fragmented index from the given path
  fragmentedIndex = pickle.load(open(fragIndexPath, "rb"))
  for word in fragmentedIndex.keys():

    # Get the first character of the word
    firstChar = word[0]
    if firstChar in indexDict:
      if word in indexDict[firstChar]:
        # If the word already exists in the index, update its postings list
        indexDict[firstChar][word].update(fragmentedIndex[word])
      else:
        # Otherwise, add a new entry for the word in the index
        indexDict[firstChar][word] = fragmentedIndex[word]
    else:
      # If there is no entry for the first character in the index, create a new one
      indexDict[firstChar] = {word:fragmentedIndex[word]}
  return indexDict

"""
tfidfSortPostings() takes in an index folder path and a corpus length, 
loads all the inverted indexes, calculates the tf-idf weight for each posting, 
and sorts the postings in each index by tf-idf weight in descending order. 
It then saves the sorted index back into the same files.
"""
def tfidfSortPostings(indexPath, corpusLen):
  for i in findAllFiles(indexPath):
    # Load the partial index file
    charDict = pickle.load(open(i, "rb"))
    for word in charDict.keys():
      # Calculate the TF-IDF score for each posting in the current word's postings list and sort them in descending order.
      wordPosting = list(charDict[word])
      for index in range(len(wordPosting)):
        wordInfo = wordPosting[index]
        wordPosting[index] = (wordInfo[0], wordInfo[1] * calcIDF(len(wordPosting), corpusLen), wordInfo[2])
      charDict[word] = sorted(wordPosting, key = lambda x:x[1], reverse = True)
    
    # Dump the updated index back to the same file
    pickle.dump(charDict, open(i, "wb"), pickle.HIGHEST_PROTOCOL)

"""
splitIndexToJson() takes in an index folder path, loads all the inverted indexes, 
and saves them in a single JSON file. It also saves a dictionary mapping each 
word to its line number in the JSON file.
"""
def splitIndexToJson(folderPath):
  wordLineDic = dict()

  # Open the output JSON file in append mode
  f = open("Index.json", "a")
  for i in findAllFiles(folderPath):
    print(i)
    # Load the partial char index file
    charDict = pickle.load(open(i, "rb"))
    for word in charDict.keys():
      # Convert the current word's postings list to JSON and write it to the output file merging index line by line
      postingJson = json.dumps(charDict[word])
      wordLineDic[word] = f.tell()
      f.write(postingJson)
      f.write("\n")
  f.close()

  # Write the starting position of each word's postings list to a separate JSON file
  with open("wordSeekPos.json", "w") as f:
    json.dump(wordLineDic, f)

"""
combineIndexChar() takes in an index folder path and a corpus length. 
It first calls findAllFiles to find the Split_Index paths, calling 
splitFragIndexByChar to split all the fragmented inverted indexes by their 
first character. It then combines all the indexes for each character into a 
single dictionary, calculates tf-idf weights for each posting, sorts the postings 
by tf-idf weight, and saves the sorted postings into separate files for each character. 
Finally, it calls splitIndexToJson to save the entire combined index as a single JSON file
without ever loading the entire index on to the ram.
"""
def combineIndexChar(folder, corpusLen):
  # Get a list of all the fragment index files in the folder
  indexPaths = findAllFiles(folder)

  # Iterate over all the fragment index files
  for i in indexPaths:
    # Split the fragment index by the first character of each word
    indexDict = splitFragIndexByChar(i)

    # Iterate over each character in the indexDict
    for char in indexDict.keys():
      # If the character file exists, load it into charDict, otherwise create an empty dict
      if path.exists(path.join("Char_Split_Index", char + ".txt")): charDict = pickle.load(open(path.join("Char_Split_Index", char + ".txt"), "rb"))
      else: charDict = {}

       # Iterate over each word in the indexDict[char]
      for word in indexDict[char]:
        # If the word exists in charDict, update its posting list with the postings from indexDict[char][word]
        # Otherwise, add the word to charDict with its postings from indexDict[char][word]
        if word in charDict:
          charDict[word].update(indexDict[char][word])
        else:
          charDict[word] = indexDict[char][word]

      # Dump the contents of charDict to the corresponding character file in "Char_Split_Index"
      pickle.dump(charDict, open(path.join("Char_Split_Index", char + ".txt"), "wb"), pickle.HIGHEST_PROTOCOL)

  # Sort the postings in each character file by tf-idf score and dump the updated index to file
  tfidfSortPostings("Char_Split_Index", corpusLen)

  # Convert the character index to a JSON format and dump it to file
  splitIndexToJson("Char_Split_Index")