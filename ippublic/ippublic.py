import Queue
import threading
from json import load
from urllib2 import urlopen, URLError
from time import time

# List of tuple (url, json, key)
# url: URL of the Web site
# json: return a JSON (True) or not (False)
# key: key of of the IP addresse in the JSON structure
urls = [('http://ip.42.pl/raw', False, None),
        ('http://httpbin.org/ip', True, 'origin'),
        ('http://jsonip.com', True, 'ip'),
        ('https://api.ipify.org/?format=json', True, 'ip')]


class Timer(object):
    """The timer class. A simple chronometer."""

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    def reset(self):
        self.start()

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time() > self.target


# called by each thread
def get_ip_public(queue, url, json=False, key=None, timeout=2):
    """Request the url service and put the result in the queue"""
    try:
        u = urlopen(url, timeout=timeout)
    except URLError:
        queue.put(None)
    else:
        # Request depend on service
        if not json:
            queue.put(u.read())
        else:
            queue.put(load(u)[key])


q = Queue.Queue()

for u, j, k in urls:
    t = threading.Thread(target=get_ip_public, args=(q, u, j, k))
    t.daemon = True
    t.start()

t = Timer(2)
ip = None
while not t.finished() and ip is None:
    if q.qsize() > 0:
        ip = q.get()
print(ip)
