import requests
from bs4 import BeautifulSoup,element


URL = "https://www.flashscore.fr/football/maroc/botola-pro/resultats/"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
page = requests.get(URL,headers=headers)
soup = BeautifulSoup(page.content, "html.parser")

print(soup)
# print(soup.find_all("div",class_="event__participant"))
