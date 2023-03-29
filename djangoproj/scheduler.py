import schedule
import time
import os

def run_spider():
    os.system('python manage.py run_spider')

# Schedule the spider to run at your desired interval (e.g., every day)
schedule.every().day.at("20:51").do(run_spider)

while True:
    schedule.run_pending()
    time.sleep(1)