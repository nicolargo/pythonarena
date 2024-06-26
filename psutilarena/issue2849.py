import psutil
import time

while True:
    print([i.idle for i in psutil.cpu_times_percent(interval=0.0, percpu=True)])
    time.sleep(2)
