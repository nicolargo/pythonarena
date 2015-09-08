import numpy as np

def isDateTimeFormat(value):
    'format: xxxx-xx-xxTxx:xx:xx.[x]*Z'
    if isString(value) == False:
        return False
    value = str.strip(value)
    if (isCastableToInteger(value[0]) == False) \
       or (isCastableToInteger(value[1]) == False) \
       or (isCastableToInteger(value[2]) == False) \
       or (isCastableToInteger(value[3]) == False) \
       or (value[4] != '-') \
       or (isCastableToInteger(value[5]) == False) \
       or (isCastableToInteger(value[6]) == False) \
       or (value[7] != '-') \
       or (isCastableToInteger(value[8]) == False) \
       or (isCastableToInteger(value[9]) == False) \
       or (value[10] != 'T') \
       or (isCastableToInteger(value[11]) == False) \
       or (isCastableToInteger(value[12]) == False) \
       or (value[13] != ':') \
       or (isCastableToInteger(value[14]) == False) \
       or (isCastableToInteger(value[15]) == False) \
       or (value[16] != ':') \
       or (isCastableToInteger(value[17]) == False) \
       or (isCastableToInteger(value[18]) == False) \
       or (value[19] != '.') \
       or (value[-1] != 'Z'):
        return False
    for i in xrange(20, len(value) - 1 - 1):
        if isCastableToInteger(value[i]) == False:
            return False
    return True

def isCastableToInteger(value):
    try:
        np.int32(value)
        return True
    except ValueError:
        return False

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
