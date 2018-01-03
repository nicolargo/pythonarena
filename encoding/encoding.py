# -*- coding: utf-8 -*-

import sys
import codecs
import locale

text_type = str
PY3 = sys.version_info[0] == 3


if not PY3:
    reload(sys)
    sys.setdefaultencoding('UTF-8')

print('sys.getdefaultencoding()     : {}'.format(sys.getdefaultencoding()))
print('locale.getpreferredencoding(): {}'.format(locale.getpreferredencoding()))
print('sys.getfilesystemencoding()  : {}'.format(sys.getfilesystemencoding()))
print('=' * 80)

with open('./test.txt') as f:
    lines = f.readlines()
lines = [line.strip('\n') for line in lines]

print('sys.stdout.encoding          : {}'.format(sys.stdout.encoding))
for line in lines:
    print('> {}'.format(line))
print('=' * 80)

sys.stdout = codecs.getwriter('utf8')(sys.stdout)
print('sys.stdout.encoding          : {}'.format(sys.stdout.encoding))
for line in lines:
    print('> {}'.format(line))
print('=' * 80)

sys.stdout = codecs.getwriter('ascii')(sys.stdout)
print('sys.stdout.encoding          : {}'.format(sys.stdout.encoding))
for line in lines:
    print('> {}'.format(line))
print('=' * 80)
