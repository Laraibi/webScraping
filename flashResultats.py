import requests
from bs4 import BeautifulSoup, element

playersInfos = []

def isNotMain(css_class):
    return "main" not in css_class and "profileTable__row--soccer" in css_class

URL = "https://www.flashscore.fr/equipe/raja-casablanca/vTnNkCKc/effectif/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
botolaProTable = soup.find("div", id="league-rHDwiDmb-table")

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

print(playersInfos)
