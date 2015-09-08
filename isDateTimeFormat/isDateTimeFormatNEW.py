import numpy as np
import re

def isDateTimeFormat(value):
    'format: xxxx-xx-xxTxx:xx:xx.[x]*Z'
    regexp = '^[0-9][0-9][0-9][0-9]\-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]\.[0-9]*Z$'
    if isString(value) == False:
        return False
    return re.search(regexp, value)

def isString(value):
    # String = basestring
    result = isinstance(value, basestring)
    #test_name = inspect.stack()[1][3]
    # print "(" + test_name + ") isString for value in " + str(type(value)) + ": " + str(result)
    return result

def main():
    for i in range(0, 500000):
        if not isDateTimeFormat('1234-56-78T90:12:23.567Z'):
            print('ERROR')
            exit(1)

if __name__ == '__main__':
    main()
