from selenium import webdriver
from fake_useragent import UserAgent
import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



def create_driver(user_id=1):
    # ua = UserAgent(platforms='pc')
    # user_agent = ua.random
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    #Настройки для Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument(f"user-agent={custom_user_agent}")
    options.add_argument("window-size=800x600")

    # Инициализация браузера
    driver = webdriver.Chrome(options=options)
    return driver
  
def saveData(items, name = 'Dataset'):
    with open(name + ".json", "w") as f:
        json.dump(items, f)
        
def get_random_chrome_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random

def getSelector(className:str, driver:webdriver.Chrome):
    return driver.find_element(By.CSS_SELECTOR, className)


