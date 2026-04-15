from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from scraping_functions import scrape_match_data
from match_data_class import *

# avoid browser being closed immediately
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.sportschau.de/live-und-ergebnisse/fussball/deutschland-bundesliga-frauen/spiele-und-ergebnisse")


scrape_match_data(driver, By, WebDriverWait, EC, sleep)


print(season)