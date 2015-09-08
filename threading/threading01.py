import threading
import time

def plugin():
    """thread worker function"""
    print('Plugin start')
    time.sleep(3)
    print('Plugin end')

t = threading.Thread(target=plugin)
t.start()
print('Main...')
