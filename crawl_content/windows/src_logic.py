import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook

def crawl_base_windows():
    # cấu hình Chrome headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    def adblock():
        try:
            popup = wait.until(EC.element_to_be_clickable((By.ID, 'zeststop')))
            popup.click()
        except TimeoutException:
            pass

    # import data from excel file
    df = pd.read_excel("../../excel/link/win_link/adobe_links.xlsx")
    links = df['Link'].tolist()

    for link in links:
        driver.get(link)
        adblock()

        container = driver.find_element(By.CSS_SELECTOR, 'div.inside-article')

        title = container.find_element(By.CSS_SELECTOR, 'h1.entry-title').text

        # TODO: bổ sung phần lấy description
        description = container.find_element(By.CSS_SELECTOR, 'div.entry-content').text

        print("📌 Title:", title)
        print("📄 Description:", description[:200], "...\n")  # in thử 200 ký tự đầu

    driver.quit()


crawl_base_windows()
