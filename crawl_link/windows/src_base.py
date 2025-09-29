import re
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from openpyxl import Workbook


def craw_link(links, path):
    options = Options()
    options.add_argument('--headless')

    result = []

    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 15)

    page_regex = re.compile(r'/page/(\d+)/?$')

    for link in links:
        base_url = f"https://diakov.net/soft/{link}/"
        driver.get(base_url)
        print(f"=== Cào category: {link} ===")

        while True:
            try:
                items = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.short-title"))
                )

                for h2 in items:
                    anchors = h2.find_elements(By.TAG_NAME, "a")
                    if len(anchors) >= 2:
                        title = anchors[1].text.strip()
                        href = anchors[1].get_attribute("href")
                        result.append([link, title, href])

                # --- xác định current page ---
                cur = driver.current_url
                m = page_regex.search(cur)
                if m:
                    current_page = int(m.group(1))
                else:
                    current_page = 1

                next_page = current_page + 1
                candidate_next = base_url if next_page == 1 else f"{base_url}page/{next_page}/"

                # chuẩn hóa
                normalize = lambda u: u.rstrip('/')
                candidate_norm = normalize(candidate_next)

                pagination_links = driver.find_elements(By.CSS_SELECTOR, "ul.pagination li a")
                found_next = any(
                    normalize(a.get_attribute("href") or "") == candidate_norm
                    for a in pagination_links
                )

                if found_next:
                    print(f"Đi sang trang {next_page} của {link}")
                    driver.get(candidate_next)
                    time.sleep(0.8)
                else:
                    print(f"Hết trang ở category {link} (đến trang {current_page})")
                    break

            except TimeoutException:
                print(f"⏳ Timeout khi load trang hiện tại của category {link}")
                break
            except Exception as e:
                print(f"Lỗi không mong muốn ở category {link}: {e}")
                break

    driver.quit()

    # ghi Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(["Category", "Title", "Link"])

    for row in result:
        ws.append(row)

    # thêm timestamp
    base, ext = os.path.splitext(path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_path = f"{base}_{timestamp}{ext}"

    folder = os.path.dirname(new_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    wb.save(new_path)
    print(f"✅ Đã lưu kết quả vào {new_path}")

