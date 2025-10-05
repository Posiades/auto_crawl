from crawl_content.windows import core

# Sử dụng
def crawl_core():
    urls = ["https://diakov.net/15771-soft-organizer-pro-956.html"]
    data = core.crawl_core(urls)
    core.save_to_excel(data, "output.xlsx")

crawl_core()