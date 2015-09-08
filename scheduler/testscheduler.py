# -*- coding: utf-8 -*-
#

import schedule
import time

def job():
    print("Start work...")
    print("End work...")

# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
