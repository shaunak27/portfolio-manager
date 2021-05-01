from bs4 import BeautifulSoup
import requests
import json


def companydetails(key):
    file = json.load(open("data/urlfile.txt"))
    url = None
    sector = None
    for i in range(len(file)):
        if file[i]["name"] == key:
            url = file[i]["url"]
            sector = file[i]["sector"]
            break
    d = dict()
    if url:
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        quote = float(soup.find(id="ltpid").get_text())
        marketcap = float(soup.find(id="MarketCap").get_text().replace(",", ""))
        pe = soup.find(id="div_rcard_more").get_text()
        pe = float(pe.split("EPS")[0].split("Ratios")[-1])
        d["cmp"] = quote
        d["marketcap"] = marketcap
        d["pe"] = pe
        d["sector"] = sector
        d["stockname"] = key
    return d
