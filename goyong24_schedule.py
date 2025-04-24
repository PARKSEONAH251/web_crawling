# scheduler.py
from datetime import datetime
import schedule
import time
from dev_jobs_goyong24_crawler import run_crawling

def job():
    if datetime.now().day == 15:
        run_crawling()

schedule.every().day.at("00:00").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
