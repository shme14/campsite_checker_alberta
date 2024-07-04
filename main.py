from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from datetime import datetime
import os
import requests

#Important stuff
url=os.environ.get('ENV_URL')
startDate = os.environ.get('ENV_START_DATE')
howLong = os.environ.get('ENV_HOW_LONG')
userName = os.environ.get('ENV_USER_NAME')
password = os.environ.get('ENV_PASSWORD')
TOKEN = os.environ.get('ENV_TOKEN')
chat_id = os.environ.get('ENV_CHATID')
delay = os.environ.get('ENV_DELAY')

def open_browser(url: str, headless=False):
    #options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    #options.add_argument("--incognito")
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        # wait for page to load and show "list button"
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.ID, 'sitelistdiv')))
        result = driver.find_element(By.CSS_SELECTOR, "#campingDate").send_keys(startDate)
        result = driver.find_element(By.CSS_SELECTOR, "#lengthOfStay").send_keys(howLong)
        result = driver.find_element(By.CSS_SELECTOR, "#search_avail")
        result.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sitelistdiv > div:nth-child(1) > div:nth-child(1)")))
        siteAvailable = (driver.find_element(By.CSS_SELECTOR, "#sitelistdiv > div:nth-child(1) > div:nth-child(1)")).text[:1]
        if((siteAvailable != "0") and (siteAvailable != "N")):
            try:
                print("Found Site! : " + siteAvailable)
                alertMe(driver, siteAvailable)

                result = driver.find_element(By.CSS_SELECTOR, ".book")
                result.click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#btnbookdates")))
                result = driver.find_element(By.CSS_SELECTOR, "#btnbookdates")
                result.click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#AemailGroup_1733152645")))
                result = driver.find_element(By.CSS_SELECTOR, "#AemailGroup_1733152645").send_keys(userName)
                result = driver.find_element(By.CSS_SELECTOR, "#ApasswrdGroup_704558654").send_keys(password)
                result = driver.find_element(By.CSS_SELECTOR, "#signinbutton > button")
                result.click()

                WebDriverWait(driver, 900).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#equip")))
                select = Select(driver.find_element(By.CSS_SELECTOR, "#equip"))
                select.select_by_value('108060')
                result = driver.find_element(By.CSS_SELECTOR, "#numoccupants").send_keys("2")
                result = driver.find_element(By.CSS_SELECTOR, "#numvehicles").send_keys("0")
                result = driver.find_element(By.CSS_SELECTOR, "#agreement").click()
                result = driver.find_element(By.CSS_SELECTOR, "#continueshop").click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#chkout")))
                result = driver.find_element(By.CSS_SELECTOR, "#chkout").click()

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cardTypeId_1")))
                select = Select(driver.find_element(By.CSS_SELECTOR, "#cardTypeId_1"))
                select.select_by_value('MAST')
                result = driver.find_element(By.CSS_SELECTOR, "#fname_1").send_keys("Jamie")
                result = driver.find_element(By.CSS_SELECTOR, "#lname_1").send_keys("Peregrym")

                input("Press Enter to continue...")
                
            except:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Something went wrong after finding a site")
                input("Press Enter to continue...")
             
        else:
            print((datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " - There are no sites available")
        
    except:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Something went wrong")
        #raise TimeoutError('Timeout loading page')

    return driver

def alertMe(driver, siteNumber):
    message = "Site number "+ siteNumber + " found! Remote in using anydesk to 1197520424 !"
    url2 = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url2).json()) # this sends the message

if __name__ == '__main__':
    while(1):
        try:
            driver = open_browser(url, headless=False)
            time.sleep(4)
            driver.quit()
        except:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - Something went wrong")
        time.sleep(int(delay))

