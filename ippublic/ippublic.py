from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()
print(my_ip)

from json import load
from urllib2 import urlopen
my_ip = load(urlopen('http://jsonip.com'))['ip']
print(my_ip)


from json import load
from urllib2 import urlopen
my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
print(my_ip)

from json import load
from urllib2 import urlopen
my_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
print(my_ip)
