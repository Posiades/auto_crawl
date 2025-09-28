import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook



def crawl_links(name_software, path_name):
    # tạo options
    options = Options()
    options.headless = True  # bật chế độ ẩn

    # khởi tạo driver với options
    driver = webdriver.Firefox(options=options)

    wait = WebDriverWait(driver, 15)
    results = []

    # xử lý popup quảng cáo nếu có
    def adblock():
        try:
            popup = wait.until(EC.element_to_be_clickable((By.ID, 'zeststop')))
            popup.click()
        except TimeoutException:
            pass

    driver.get("https://karanpc.com/windows/")
    adblock()

    for app in name_software:
        print(f"🔹 Crawl {app} (link đầu tiên)")
        container = wait.until(EC.presence_of_element_located((By.ID, "ajaxsearchlite2")))
        search_input = container.find_element(By.CSS_SELECTOR, "input.orig")
        search_input.clear()
        search_input.send_keys(app.lower())
        time.sleep(1)

        search_btn = container.find_element(By.CSS_SELECTOR, "button.promagnifier")
        search_btn.click()
        time.sleep(2)

        wait.until(EC.presence_of_element_located((By.ID, "main")))

        # lấy link đầu tiên
        links = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title a")
        if links:
            href = links[0].get_attribute("href")
            if href:
                results.append((app, href))

    driver.quit()

    # lưu ra Excel
    wb = Workbook()
    ws = wb.active
    ws.title = f"{path_name}"
    ws.append(["Phần mềm", "Link"])
    for app, link in results:
        ws.append([app, link])
    output = f"excel/link/win_link/{path_name}.xlsx"
    os.makedirs(os.path.dirname(output), exist_ok=True)  # tạo folder nếu chưa có
    wb.save(output)
    print(f"Đã lưu {len(results)} link vào {output}")


