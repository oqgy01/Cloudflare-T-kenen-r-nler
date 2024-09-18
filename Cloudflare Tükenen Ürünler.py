#Doğrulama Kodu
import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import pandas as pd
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from io import BytesIO
import os
import numpy as np
import shutil
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import xml.etree.ElementTree as ET
import warnings
from colorama import init, Fore, Style
import openpyxl
from openpyxl import load_workbook
import threading
import tkinter as tk
from tkinter import simpledialog
import chromedriver_autoinstaller



chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=1') 
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  
driver = webdriver.Chrome(options=chrome_options)  
login_url = "https://task.haydigiy.com/kullanici-giris/?ReturnUrl=%2Fadmin"
driver.get(login_url)
email_input = driver.find_element("id", "EmailOrPhone")
email_input.send_keys("mustafa_kod@haydigiy.com")
password_input = driver.find_element("id", "Password")
password_input.send_keys("123456")
password_input.send_keys(Keys.RETURN)


while True:
    try:

        desired_page_url = "https://task.haydigiy.com/admin/product/bulkedit/"
        driver.get(desired_page_url)
        
        time.sleep(5)
        
        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'k-formatted-value'))
            )
            input_element.clear()
            input_element.send_keys("1")
        except Exception as e:
            print(f"Hata: {e}")

        time.sleep(1)

        category_select = Select(driver.find_element("id", "SearchInCategoryIds"))
        category_select.select_by_value("521")

        time.sleep(1)

        all_remove_buttons = driver.find_elements(By.XPATH, "//span[@class='select2-selection__choice__remove']")
        if len(all_remove_buttons) > 1:
            second_remove_button = all_remove_buttons[1]
            second_remove_button.click()

        time.sleep(1)

        search_button = driver.find_element(By.ID, "search-products")
        search_button.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Category_Update")))
        driver.execute_script("arguments[0].click();", checkbox)

        time.sleep(1)

        category_id_select = driver.find_element(By.ID, "CategoryId")
        category_id_select = Select(category_id_select)
        category_id_select.select_by_value("521")

        time.sleep(1)

        category_transaction_select = driver.find_element(By.ID, "CategoryTransactionId")
        category_transaction_select = Select(category_transaction_select)
        category_transaction_select.select_by_value("1")

        time.sleep(1)

        try:
            save_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'btn-primary'))
            )
            driver.execute_script("arguments[0].click();", save_button)
        except Exception as e:
            print(f"Hata: {e}")


        time.sleep(100)

        

        def fetch_and_send_links():
            try:
                # XML'den linkleri al
                xml_url = "https://task.haydigiy.com/FaprikaXml/OF2CIP/1/"
                response = requests.get(xml_url)
                response.raise_for_status()

                root = ET.fromstring(response.content)
                urls = [elem.text for elem in root.findall('.//link')]

                all_links = []

                for url in urls:
                    full_url = url + "/?product=True"
                    page_response = requests.get(full_url)
                    page_response.raise_for_status()

                    soup = BeautifulSoup(page_response.content, 'html.parser')
                    same_products_div = soup.find('div', class_='same-products-item')

                    if same_products_div:
                        hrefs = [a['href'] for a in same_products_div.find_all('a', href=True)]
                        full_hrefs = [f"https://www.haydigiy.com{href}" for href in hrefs]
                        all_links.extend(full_hrefs)

                # Cloudflare API'ye istek gönder
                cf_url = "https://api.cloudflare.com/client/v4/zones/469d52dc478eb1a2e1864dc0b3f548ac/purge_cache"
                headers = {
                    "Content-Type": "application/json",
                    "X-Auth-Email": "erkan@haydigiy.com",
                    "X-Auth-Key": "c45a4d56745100a8568a2e9e7a00948f23b4e"
                }
                data = {
                    "files": all_links
                }

                # Gönderilen linkleri yazdırma
                print("API'ye gönderilen linkler:")
                for link in all_links:
                    print(link)

                cf_response = requests.post(cf_url, headers=headers, json=data)
                cf_response.raise_for_status()

            except requests.exceptions.HTTPError as e:
                print(f"Ürün Yok: {e}, başa dön")
                time.sleep(3)  # 3 saniye bekle

        if __name__ == "__main__":
            fetch_and_send_links()




        # Kategorinin Dışında Kalan Stoğu 0 Olan Ürünleri Kategoriye Alma
        search_not_in_category_select = Select(driver.find_element("id", "SearchNotInCategoryIds"))
        search_not_in_category_select.select_by_value("521")
        
        time.sleep(1)

        third_span = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.select2-selection__choice__remove')))[2]
        third_span.click()

        time.sleep(5) #2 saniye bekle

        try:
            input_elements = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, 'k-formatted-value'))
            )
            input_element = input_elements[1]
            input_element.clear()
            input_element.send_keys("0")
        except Exception as e:
            print(f"Hata: {e}")

        time.sleep(1)

        search_button = driver.find_element(By.ID, "search-products")
        search_button.click()

        time.sleep(1)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)

        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Category_Update")))
        driver.execute_script("arguments[0].click();", checkbox)

        time.sleep(1)

        category_id_select = driver.find_element(By.ID, "CategoryId")
        category_id_select = Select(category_id_select)
        category_id_select.select_by_value("521")

        time.sleep(1)

        try:
            save_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'btn-primary'))
            )
            driver.execute_script("arguments[0].click();", save_button)
        except Exception as e:
            print(f"Hata: {e}")


    except Exception as e:
        print(f"Beklenmedik hata: {e}, başa dön")