# The following resources were useful
# - https://stackoverflow.com/questions/44119081/how-do-you-fix-the-element-not-interactable-exception
import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def generate_caption(img_path="img_to_caption.png"):
    try:
        img_path = os.getcwd() + '/' + img_path
        driver, api_path = webdriver.Chrome(), "https://pallyy.com/tools/image-description-generator"
        driver.get(api_path)
        # time.sleep(5)
        # driver.get(api_path)
        time.sleep(3)
        upload = driver.find_element('tag name', 'input')
        upload.send_keys(img_path)
        time.sleep(25)
        hit_button = driver.find_element('class name', 'generate-button')
        hit_button.click()
        time.sleep(5)
        clipboard_copy_button = driver.find_elements('class name', 'tweet__button-copy')[1]
        clipboard_copy_button.click()
        time.sleep(5)
        res_str = pyperclip.paste()

        return res_str
    except:
        return "I'm tired, please try it later."

