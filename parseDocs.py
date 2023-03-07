from bs4 import BeautifulSoup
import lxml
import json
import re

def getStrings(filename: str) -> list:
  with open(filename) as f:
    data = json.load(f)
    url = data["url"]
    soup = BeautifulSoup(data["content"], features="html.parser")
    text = soup.text.lower().strip()

    importantWords = set()
    for i in soup.find_all(["Title", "b", "strong", "h1", "h2", "h3"]):
      importantWords.add(i.get_text())

  return url, re.findall("['`0-9a-zA-Z]+", text), importantWords
