import Queue
import threading
from json import load
from urllib2 import urlopen


# called by each thread
def get_ip_public(q, url):
    if url == 'http://ip.42.pl/raw':
        q.put(urlopen(url).read())
    elif url == 'http://httpbin.org/ip':
        q.put(load(urlopen(url))['origin'])
    elif url == 'http://jsonip.com' or url == 'https://api.ipify.org/?format=json':
        q.put(load(urlopen('http://jsonip.com'))['ip'])

urls = ['http://ip.42.pl/raw', 'http://httpbin.org/ip', 'http://jsonip.com', 'https://api.ipify.org/?format=json']


q = Queue.Queue()

for u in urls:
    t = threading.Thread(target=get_ip_public, args=(q, u))
    t.daemon = True
    t.start()

ip = q.get()
print(ip)
