from apscheduler.schedulers.blocking import BlockingScheduler
import time
from crawl_link import windows as wl
from crawl_content import windows as wc

def main():
    # crawl link game and windows, macos app
    wl.link_app()




if __name__ == '__main__':
    main()

    scheduler = BlockingScheduler()

    # Lên lịch chạy main() mỗi 7 ngày
    scheduler.add_job(main, 'interval', days=7)

    print("Bắt đầu chạy lịch...")
    scheduler.start()