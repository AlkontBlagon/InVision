from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from helper import create_driver 
import time



def start_passerTg(info, driver:webdriver.Chrome):
    driver.get(info["src"])
    #subscrub = getTgSubs(driver)
    views = getTgViews(driver)
    return{ 
        "platform": 'TG',
        'subscrube': info['subscriber'],
        "views": views
    }
    
def start_passerVk(info, driver:webdriver.Chrome):
    driver.get(info["src"])
    views = getVkViews(driver)
    return{ 
        "platform": 'VK',
        'subscrube': info['subscriber'],
        "views": views
    }

def getTgSubs(driver:webdriver.Chrome):
    text= driver.find_element(By.CSS_SELECTOR, '.tgme_channel_info_counter').get_attribute('outerText')
    text= text.replace(' Subscribers', '')     
    Cont= CountFormat(text)
    return Cont  

def CountFormat(text: str):
    view = text.replace("млн", "")
    view = view.replace("тыс.", "")
    view = view.replace("M", "")
    view = view.replace(",", ".")
    view = view.replace("K", "")
    if text.find('M') != -1:
        view = float(view) * 1000000
    elif text.find('K') != -1:
        view = float(view) * 1000
    elif text.find('млн') != -1:
        view = float(view) * 1000000
    elif text.find('тыс.') != -1:
        view = float(view) * 1000
    return view

def getTgViews(driver:webdriver.Chrome):
    result= driver.find_elements(By.CSS_SELECTOR, '.tgme_widget_message_views')
    views= []    
    for view in result[::-1][:10]: 
       text= view.get_attribute("textContent")
       Cont= CountFormat(text)
       views.append(Cont)

    return views[::-1]

def getVkSubs(driver:webdriver.Chrome):
    return driver.find_element(By.CSS_SELECTOR, '.redesigned-group-subscribers').get_attribute("outerHTML")

def getVkViews(driver:webdriver.Chrome):
    scrollDocument(driver)
    result= driver.find_elements(By.CSS_SELECTOR, '._views')
    views= []    
    for view in result[:10][::-1]: 
       text= view.get_attribute("textContent")
       Cont= CountFormat(text)
       views.append(Cont)

    return views[::-1]
def scrollDocument(driver : webdriver.Chrome):  
    last_height = driver.execute_script("return document.body.scrollHeight")
    count_scroll = 30
    count = 0
    while True: 
        # Прокрутка вниз 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        # Пауза, пока загрузится страница. 
        time.sleep(1)
        if count > count_scroll:
            break
        count = count + 1

def getURL(driver:webdriver.Chrome):
    return driver.find_element(By.CSS_SELECTOR, '.t-store__tabs__content a').get_attribute("href")

def OpenYANDEX(driver: webdriver.Chrome, name: str, platform: str):
    driver.get("https://ya.ru/")
    site = 't.me/s/' if platform == 'telegram' else f'{platform}.com'
    isCaptcha = True
    searchInput = False
    while isCaptcha:
        captcha = driver.find_elements(By.CLASS_NAME, 'CaptchaLinks-Links')
        if captcha:
            time.sleep(5)
        else:
            if searchInput:
                captcha = driver.find_elements(By.CLASS_NAME, 'CaptchaLinks-Links')
                if captcha:
                    time.sleep(2)
                else:
                    return True
            else:
                elem = driver.find_element(By.CLASS_NAME, 'search3__input')
                elem.send_keys(f'site:{site} ' + name + Keys.RETURN)
                searchInput = True
                time.sleep(2)
    return False


def searchResult(driver: webdriver.Chrome, platform: str):
    time.sleep(1)
    row = driver.find_element(By.CSS_SELECTOR,
                              '.Organic.organic.Typo.Typo_text_m.Typo_line_s')
    src = row.find_element(
        By.CSS_SELECTOR,
        'a.Link.Link_theme_normal.OrganicTitle-Link.organic__url.link'
    ).get_attribute('href')
    subscriber = 0
    elements = row.find_elements(By.CSS_SELECTOR, '.KeyValue-Row')

    for element in elements:
        try:
            title = element.find_element(By.CSS_SELECTOR,
                                         '.KeyValue-ItemTitle').text
            value = element.find_element(By.CSS_SELECTOR,
                                         '.KeyValue-ItemValue').text
            if (title == "Подписчиков:"):
                value= value.replace(" ","")
                subscriber = CountFormat(value)

        finally:
            continue
    return {'src': src, 'subscriber': subscriber}
def run_paser(name: str):
    data=[]
    driver=create_driver()
    if OpenYANDEX(driver, name,"vk"): 
        info= searchResult(driver,'vk')
        result= start_passerVk(info,driver)
        data.append(result)

    if OpenYANDEX(driver, name,"telegram"): 
        info= searchResult(driver,'telegram')
        result= start_passerTg(info,driver)
        data.append(result)
    return data
