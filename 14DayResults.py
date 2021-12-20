# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.common.exceptions import TimeoutException
import json
import time

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d_%m_%YT%Hh%Mm%Ss")
fileName="14DayResult"+dt_string
# time.get_clock_info
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['enable-webgl-developer-extensions'] = True
caps['enable-webgl-draft-extensions'] = True
caps['enable-drdc'] = True
driver = webdriver.Chrome(
    executable_path='chromedriver.exe', desired_capabilities=caps)

# print(caps)
driver.get('https://www.flashscore.fr/')
driver.maximize_window()
# exit()
timeout = 90
try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "event__match")))
except TimeoutException:
    driver.quit()

driver.find_element(By.CLASS_NAME, "calendar__datepicker").click()
time.sleep(5)
driver.find_element(By.CLASS_NAME, "day").click()
try:
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "event__match")))
except TimeoutException:
    driver.quit()
# exit()
matchsList = []


for x in range(14):
    print(f"==========Day : {x+1}")

    timeout = 90
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "event__match")))
    except TimeoutException:
        driver.quit()

    eventsElements = driver.find_elements(
        By.CSS_SELECTOR, "div.event__match--twoLine,div.event__header")
    # eventsElements = driver.find_elements(
    #     By.XPATH, "//div[@class='event__match--twoLine' or @class='event__header']")
    # print(len(eventsElements))
    day = driver.find_element(
        By.CSS_SELECTOR, "div.calendar__datepicker").text.split(" ")[0]
    matchCount = 0
    for x in range(len(eventsElements)):
        # for x in range(100):
        event = eventsElements[x]
        if "event__header" in event.get_attribute("class").split(" "):
            league = event.find_element(
                By.CLASS_NAME, "event__title--name").text
            country = event.find_element(
                By.CLASS_NAME, "event__title--type").text.replace("\"", "")
            print(f"crawling league : {league} // country :{country}")
            continue
        else:
            match = event
        matchCount += 1
        home = match.find_elements(By.CLASS_NAME, "event__participant--home")[
            0].text if len(match.find_elements(By.CLASS_NAME, "event__participant--home")) > 0 else ""
        away = match.find_elements(By.CLASS_NAME, "event__participant--away")[
            0].text if len(match.find_elements(By.CLASS_NAME, "event__participant--away")) > 0 else ""
        time = match.find_elements(By.CLASS_NAME, "event__time")[0].text if len(match.find_elements(
            By.CLASS_NAME, "event__time")) > 0 else ""
        score = {
            "home": 0,
            "away": 0,
        }
        score["away"] = match.find_elements(By.CLASS_NAME, "event__score--away")[0].text  if len(match.find_elements(
            By.CLASS_NAME, "event__score--away")) > 0 else ""
        score["home"] = match.find_elements(By.CLASS_NAME, "event__score--home")[0].text if len(match.find_elements(
            By.CLASS_NAME, "event__score--home")) > 0 else ""
        isEnded = "unKnown"
        if len(match.find_elements(By.CLASS_NAME, "event__stage--block")) > 0:
            isEnded = True if match.find_element(
                By.CLASS_NAME, "event__stage--block").text == "Terminé" else False

        matchsList.append({"home": home,
                           "away": away,
                           "time": time.replace("\nRFS", ""),
                           "league": league,
                           "country": country,
                           "score": score,
                           "Day": day,
                           "Ended": isEnded
                           })
    print(f"match count :{matchCount}")
    driver.find_element(By.CLASS_NAME, "calendar__direction--tomorrow").click()

with open(fileName+'.json', 'w', encoding='utf8') as json_file:
    json.dump(matchsList, json_file, ensure_ascii=False)
json_file.close()
driver.quit()
