import json
import re
from collections import defaultdict
from timeit import default_timer as timer
from nltk.stem import PorterStemmer
import math
import tkinter as tk

"""
search() seeks posting in Index file loading a singluar line with 
the posting performing a search based on the user query,
and returns a list of top 10 urls that best match the query based on 
cosine similarity.
"""
def search(query : str, porterStemmer, index, wordLineDic) -> list:

    #tokenizing & stemming user query
    ps = porterStemmer
    text = query.lower().strip()

    # find all alphanumeric words using regular expression matching
    words = re.findall("['`0-9a-z]+", text)

    # create a defaultdict to count the frequency of each stemmed word in the quer
    queryDic = defaultdict(int)
    for i in words:
        queryDic[ps.stem(i)] += 1

    # compute cosine scores for each document
    scores = defaultdict(float)

    for token in queryDic.keys():
        # calculate the TF-IDF score for each query term
        tfidfQ = (queryDic[token] / len(queryDic)) * math.log(1 / (len(queryDic) + 1))

        # retrieve the posting list for the current term from the index file
        postings = []
        if token in wordLineDic:
            index.seek(wordLineDic[token])

            postings = json.loads(index.readline().strip())

        # get the TF-IDF score for each document containing the current term and update the cosine score for the document
        # and apply the BM25 normalization if the term is an important word
        for i in postings:
            tfidfD = i[1]
            if i[2]: tfidfD *= 0.75
            
            scores[i[0]] += tfidfQ * tfidfD
    
    # normalize the cosine scores by dividing them by the length of the query dictionary
    for doc in scores.keys():
        scores[doc] = scores[doc] / len(scores)
    
    # sort the documents by their cosine scores in ascending order and return the top 10 documents
    urls = sorted([(k, v) for k, v in scores.items()], key = lambda x: x[1])
    if len(urls) == 0: return []
    if len(urls) < 10: return [urls[i][0] for i in range(len(urls))]
    return [urls[i][0] for i in range(10)]

def gui(ps, index, wordLineDic):
    # Create a GUI window
    window = tk.Tk()
    window.geometry("800x500")

    # Create labels, an entry, a button, and a text box for the search results
    label = tk.Label(text = "Please type in Query and Press Search")
    entry = tk.Entry(width=50)
    button = tk.Button(text="Search")
    label2 = tk.Label(text = "No Query Yet")
    results = tk.Text()
    
    # Add the widgets to the window
    label.pack(padx=5, pady=5)
    entry.pack(padx=5, pady=5)
    button.pack(padx=5, pady=5)
    label2.pack(padx=5, pady=5)
    results.pack(padx=20, pady=20)

    # Define a function to handle a button click event on search button
    def handle_click(event):
        # Get the user query from the entry widget
        query = entry.get()
        entry.delete(0, tk.END)

        # If the query is empty, display a message and return
        if not query.strip():
            label2.config(text = f"Query was empty")
            results.config(state='normal')
            results.delete("1.0", tk.END)
            results.config(state='disabled')
            return
        
        # Perform the search and display the results, while also timing the search
        start = timer()
        
        searchResults = search(query, ps, index, wordLineDic)

        end = timer()

        displayText = ""
        for i in searchResults:
            displayText += i + "\n"

        results.config(state='normal')
        results.delete("1.0", tk.END)
        results.insert("1.0", displayText.strip())

        end = timer()

        label2.config(text = f"Query: {query} - Top 10 Results - Time Taken: {(end - start):.5f} s")

    button.bind("<Button-1>", handle_click)

    window.mainloop()

def termnal(ps, index, wordLineDic):
    prompt = "Please Input Query or Type quit:"
    
    queryNum = 0
    
    while (True):
        userInput = str(input(prompt))
        
        start = timer()

        if userInput == "quit": break
        
        queryNum += 1

        urlPaths = search(userInput, ps, index, wordLineDic)

        print(f"Query {queryNum} - Top 10 Results")
        for i in urlPaths:
            print(i)

        end = timer()

        print(f"Time Taken: {(end - start):.5f}")

        print()

"""
promptSearches(ui) function is the main entry point to the search engine. 
It first loads the dictionary wordLineDic that maps each word in the index to 
its position in the index file. It then opens the index file and creates 
an instance of the PorterStemmer class. Launches the user interface based on the value of the ui
"""
def promptSearches(ui) -> None:

    # load the dictionary mapping words to their positions in the index
    wordLineDic = None
    with open("wordSeekPos.json", "r") as f:
        wordLineDic = json.load(f)

    # open the index file, witout loading it into memory
    index = open("Index.json", "r")

    ps = PorterStemmer()

    # launch the user interface (either GUI or terminal-based)
    if ui == "GUI":
        gui(ps, index, wordLineDic)
    else:
        termnal(ps, index, wordLineDic)

    # close the index file
    index.close()
    print("User Quit Searching")

if __name__ == "__main__": 
    promptSearches("GUI")