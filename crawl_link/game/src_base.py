import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook


def crawl_game(path_name):

    options = Options()
    options.add_argument("-headless")  # chạy ẩn

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 15)
    result = []

    print("Truy cập đến trang web")
    driver.get(f"https://oceanofgames.com/category/{path_name}/")
    time.sleep(3)

    while True:
        # lấy danh sách link
        print("Đang lấy link.....")
        elements = driver.find_elements(By.CSS_SELECTOR, "div.post-details h2.title a")
        for item in elements:
            link = item.get_attribute("href")
            result.append(link)

        # thử click nút Next
        try:
            print("Đang qua trang tiếp theo")
            next_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next"))
            )
            next_button.click()
            time.sleep(2)
        except TimeoutException:
            break

    # lưu Excel
    wb = Workbook()
    ws = wb.active
    ws.title = f"Game {path_name}"

    for item in result:
        ws.append([item])  # phải là list

    output = f"excel/link/game_link/{path_name}.xlsx"
    os.makedirs(os.path.dirname(output), exist_ok=True)
    wb.save(output)
    print(f"Đã lưu {len(result)} link vào {output}")

    driver.quit()

