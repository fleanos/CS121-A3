import json
import re
from collections import defaultdict
from timeit import default_timer as timer
from nltk.stem import PorterStemmer
import math
import tkinter as tk


def search(query : str, porterStemmer, index, wordLineDic) -> list:

    #tokenizing & stemming user query
    ps = porterStemmer
    text = query.lower().strip()
    words = re.findall("['`0-9a-z]+", text)

    queryDic = defaultdict(int)
    for i in words:
        queryDic[ps.stem(i)] += 1

    #computing cosine scores
    scores = defaultdict(float)

    for token in queryDic.keys():
        tfidfQ = (queryDic[token] / len(queryDic)) * math.log(1 / (len(queryDic) + 1))

        postings = []
        if token in wordLineDic:
            index.seek(wordLineDic[token])

            postings = json.loads(index.readline().strip())

        for i in postings:
            tfidfD = i[1]
            if i[2]: tfidfD *= 0.75
            
            scores[i[0]] += tfidfQ * tfidfD
        
    for doc in scores.keys():
        scores[doc] = scores[doc] / len(scores)
    
    urls = sorted([(k, v) for k, v in scores.items()], key = lambda x: x[1])
    if len(urls) == 0: return []
    if len(urls) < 10: return [urls[i][0] for i in range(len(urls))]
    return [urls[i][0] for i in range(10)]

def gui(ps, index, wordLineDic):
    window = tk.Tk()
    window.geometry("800x500")

    label = tk.Label(text = "Please type in Query and Press Search")
    entry = tk.Entry(width=50)
    button = tk.Button(text="Search")
    label2 = tk.Label(text = "No Query Yet")
    results = tk.Text()
    

    label.pack(padx=5, pady=5)
    entry.pack(padx=5, pady=5)
    button.pack(padx=5, pady=5)
    label2.pack(padx=5, pady=5)
    results.pack(padx=20, pady=20)

    def handle_click(event):
        query = entry.get()
        entry.delete(0, tk.END)
        if not query.strip():
            label2.config(text = f"Query was empty")
            results.config(state='normal')
            results.delete("1.0", tk.END)
            results.config(state='disabled')
            return
        
        start = timer()
        
        displayText = ""
        for i in search(query, ps, index, wordLineDic):
            displayText += i + "\n"

        results.config(state='normal')
        results.delete("1.0", tk.END)
        results.insert("1.0", displayText.strip())

        end = timer()

        label2.config(text = f"Query: {query} - Top 10 Results - Time Taken: {end - start} ms")

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

        print(f"Time Taken: {end - start}")

        print()

def promptSearches(ui) -> None:

    wordLineDic = None
    with open("wordSeekPos.json", "r") as f:
        wordLineDic = json.load(f)

    index = open("Index.json", "r")

    ps = PorterStemmer()

    if ui == "GUI":
        gui(ps, index, wordLineDic)
    else:
        termnal(ps, index, wordLineDic)

    index.close()
    print("User Quit Searching")

if __name__ == "__main__": 
    promptSearches("GUI")