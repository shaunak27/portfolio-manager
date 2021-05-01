from bs4 import BeautifulSoup
import requests
import json


def companynews(stockname):
    file = json.load(open("data/urlfile.txt"))
    url = None

    for i in range(len(file)):
        if file[i]["name"] == stockname:
            url = file[i]["url"]
            break

    h = []

    if url:
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a"):
            p = link.get("href")
            if p[0] == "h" and p[4] == "s" and p[28] == "n" and p[33] == "b":
                p = p.split("/")[5]
                h.append(p)

    return h
