# -*- coding: utf-8 -*-

from io import open
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
elif PY2:
    text_type = unicode
    binary_type = str


def to_ascii(s, errors='replace'):
    if isinstance(s, binary_type):
        return unicode(s, errors=errors)
    return s.encode('ascii', errors=errors).decode()


with open('./test.txt', encoding='utf-8') as f:
    lines = f.readlines()
lines = [line.strip('\n') for line in lines]

for line in lines:
    print('{}'.format(to_ascii(line)))
