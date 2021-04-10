from bs4 import BeautifulSoup
import requests

html = requests.get('http://money.rediff.com/companies/Tata-Motors-Ltd/10510008').content

soup = BeautifulSoup(html, 'html.parser')
quote = float(soup.find(id='ltpid').get_text())
marketcap =  soup.find(id='MarketCap').get_text()
print("cmp ="+str(quote))
print("marketcap ="+marketcap)

pe = soup.find(id='div_rcard_more').get_text()
pe = pe.split('EPS')[0]
print(pe)
