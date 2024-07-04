from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

#Important stuff
url=os.environ.get('ENV_URL')
driver = webdriver.Firefox()
driver.get(url)