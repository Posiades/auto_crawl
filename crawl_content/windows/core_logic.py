import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def crawl_base_windows():
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 40)

    df = pd.read_excel("../../excel/link/win_link/adobe_links.xlsx")
    links = df['Link'].tolist()

    results = []

    for url in links:
        print(f"🔎 Crawling: {url}")
        driver.get(url)

        # scroll nhiều lần để chắc chắn load hết
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        try:
            container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.inside-article"))
            )
            title = container.find_element(By.CSS_SELECTOR, "h1.entry-title").text

            content_div = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.entry-content"))
            )

            # Lấy từng đoạn văn <p>
            paragraphs = content_div.find_elements(By.TAG_NAME, "p")
            description = "\n\n".join(p.text for p in paragraphs if p.text.strip())

            results.append({"Title": title, "Content": description})
            print(f"✅ Done: {title}")

        except TimeoutException:
            print(f"❌ Timeout: {url}")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            continue

    driver.quit()

    output_path = "../../excel/content/adobe_articles_full.xlsx"
    pd.DataFrame(results).to_excel(output_path, index=False)
    print(f"🎉 Đã lưu {len(results)} bài vào {output_path}")

crawl_base_windows()
