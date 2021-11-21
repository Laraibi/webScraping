# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

# URL = "https://www.flashscore.fr/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

# }
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get('https://www.flashscore.fr/')
# driver.get('https://www.kooora.com/?region=-1&area=0')
timeout = 90
try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "event__match")))
except TimeoutException:
    driver.quit()


matchsList = []
matchsElemnts = driver.find_elements(By.CLASS_NAME, "event__match--twoLine")
for x in range(5):
    match = matchsElemnts[x]

    # print(match.text)
    home = match.find_elements(By.CLASS_NAME, "event__participant--home")[
        0].text if len(match.find_elements(By.CLASS_NAME, "event__participant--home")) > 0 else ""
    away = match.find_elements(By.CLASS_NAME, "event__participant--away")[
        0].text if len(match.find_elements(By.CLASS_NAME, "event__participant--away")) > 0 else ""
    time = match.find_elements(By.CLASS_NAME, "event__time")[0].text if len(match.find_elements(
        By.CLASS_NAME, "event__time")) > 0 else ""
    # league = match.find_elements(
    #     By.XPATH, "//div[@class='event__header'][1]")[0].text
    league = match.find_elements(
        By.XPATH, "//preceding::div[@class='event__header']")[0].text
    print(league)
    matchsList.append({"home": home,
                       "away": away,
                       "time": time,
                       })
exit()
# print(matchsList)
jsonStr = json.dumps(matchsList)
jsonFile = open("matchsToDay.json", "w")
jsonFile.write(jsonStr)
jsonFile.close()
driver.quit()
