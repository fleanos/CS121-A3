from bs4 import BeautifulSoup
import lxml
import json
import re

"""
getStrings() is designed to read a JSON file containing information about a webpage, 
extract its text content, and return a list containing the URL of the page, a list of words 
from the text content of the page, and a set of important words from the page.
"""
def getStrings(filename: str) -> list:
  # Open the file and load its contents as JSON data
  with open(filename) as f:
    data = json.load(f)

    # Extract the URL of the webpage
    url = data["url"]

    # Use BeautifulSoup to parse the HTML content of the webpage and extract its text
    soup = BeautifulSoup(data["content"], features="html.parser")
    text = soup.text.lower().strip()

    # Extract important words from the webpage by searching for specific HTML tags
    importantWords = set()
    for i in soup.find_all(["Title", "b", "strong", "h1", "h2", "h3"]):
      importantWords.add(i.get_text())

  # Return URL of the page, a list of words from the text content of the page, and a set of important words from the page.
  return url, re.findall("['`0-9a-zA-Z]+", text), importantWords
