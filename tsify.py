from sys import argv
import re
from bs4 import BeautifulSoup
import requests
import urllib.parse
import urllib.request
import random

def Thesaurise(word):
    html = ""
    beautsoup = ""
    found = False
    try:
        with urllib.request.urlopen("https://www.thesaurus.com/browse/" + word) as response:
            html = response.read()
            if b"MOST RELEVANT" in html:
                html = html.split(b"MOST RELEVANT")[0]
                beautsoup = BeautifulSoup(html, 'html.parser')
                found = True
    except:
        return word
    
    synonyms = []
    if found:
        for word in beautsoup.find_all("a"):
            if word.get("href") != None:
                if word.get("href").startswith("/browse/"):
                    synonyms.append(word.text)
    if(len(synonyms) < 3):
        return random.choice(synonyms)
    return random.choice(synonyms[1:3])

song = ' '.join([s for s in argv[1:]])
url = f"https://canarado-lyrics.p.rapidapi.com/lyrics/{urllib.parse.quote(song)}"

# shush
headers = {
    'x-rapidapi-host': "canarado-lyrics.p.rapidapi.com",
    'x-rapidapi-key': "6c7f85f5b2msh9d4b133d4c2cce9p1fba4cjsn6e0ebdf569d1" #here, have my key
}

response = requests.request("GET", url, headers=headers)
lyrics = response.json()["content"][0]["lyrics"] #shut up
lyrics = re.sub(r'\[.+?\]\n', '', lyrics) #remove the [chorus] [verse 1] etc thingies
lyrics.strip()

words = []
original_words = []
count = 0

for w in lyrics.split():
    count += 1
    w.strip('\'\"., ')
    original_words.append(w)
    if(count % 3 == 0):
        if(len(w) < 4):
            count -= 1
        else:
            w = Thesaurise(w)
    words.append(w)

out = ""
word_iterator = 0
word_length = len(words)
n = len(lyrics)
i = 0

while True:
    if word_iterator >= word_length or i >= n:
        break

    c = lyrics[i]

    if c.isalpha():
        i += len(original_words[word_iterator])
        out += words[word_iterator]
        word_iterator += 1
    else:
        out += c
        i += 1

print(out)
