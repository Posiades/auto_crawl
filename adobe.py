import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook

# danh sách phần mềm Adobe
adobe_apps = [
    "Acrobat", "Photoshop", "Illustrator", "After Effects", "Premiere Pro",
    "Lightroom", "InDesign", "Animate", "Audition", "Bridge", "Dreamweaver",
    "Fresco", "Character Animator", "Dimension", "Media Encoder", "XD"
]

def crawl_adobe_links(output="cache_excel/adobe_link_crawl.xlsx"):
    driver = webdriver.Firefox()
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

    for app in adobe_apps:
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
    ws.title = "adobe_links"
    ws.append(["Phần mềm", "Link"])
    for app, link in results:
        ws.append([app, link])
    wb.save(output)
    print(f"Đã lưu {len(results)} link Adobe vào {output}")


