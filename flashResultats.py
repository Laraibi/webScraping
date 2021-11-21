import requests
from bs4 import BeautifulSoup, element
import json

playersInfos = []

def isNotMain(css_class):
    return "main" not in css_class and "profileTable__row--soccer" in css_class
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
URL = "https://www.flashscore.fr/equipe/wydad/2yuuwjkA/effectif/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
botolaProTable = soup.find("div", id="league-rHDwiDmb-table")
# botolaProTable = soup.find("div", id="league-tdkpynmB-table")
#

playersElements = botolaProTable.find_all("div", class_="tableTeam__squadInfo")
for player in playersElements:
    Number = player.find("div", class_="tableTeam__squadNumber").text
    Name = ""
    if len(player.select("a")) > 0:
        Name = player.select("a")[0].text
    if(Name and Number):
        parent = player.parent
        stats = parent.find("div", class_="playerTable__icons--squad")
        listStats = []
        for stat in stats.children:
            if(stat != '\n'):
                listStats.append(stat.text)

        objStats = {"age": listStats[0],
                    "played": listStats[1],
                    "goals": listStats[2],
                    "yCards": listStats[3],
                    "rCards": listStats[4]}
        playersInfos.append(
            {"name": Name, "number": Number, "stats": objStats})

# print(playersInfos)
jsonStr = json.dumps(playersInfos)
print(jsonStr)
jsonFile = open("dataClub.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()