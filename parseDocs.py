"Parse All text in doc and return as list with all strings"
# Use beautifulsoup, go through every single tag, and then parse

from bs4 import BeautifulSoup  #extracting links
import lxml
import json
import re

def getStrings(filename: str) -> list:
  with open(filename) as f:
    data = json.load(f)
    soup = BeautifulSoup(data["content"], features="xml")
    text = soup.text.lower().strip().split()
    text = [re.split("[^’'0-9a-zA-Z]+", word) for word in text]
    return [re.sub("[’']+", "", word) for wordlist in text for word in wordlist if word != "" and len(word) >= 1]
