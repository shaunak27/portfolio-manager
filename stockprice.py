from bs4 import BeautifulSoup
import requests

html = requests.get('http://money.rediff.com/companies/3m-India-Ltd/17010019').content

soup = BeautifulSoup(html, 'html.parser')
quote = float(soup.find(id='ltpid').get_text())

print(quote)
