import os
import psutil

def get_mem():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0] / float(2 ** 20)

def main(arg):
    print get_mem()
    del arg
    print get_mem()

if __name__ == '__main__':
    print get_mem()
    biglist = [([], [], [], [], []) for _ in xrange(100000)]
    main(biglist)
    del biglist
    print get_mem()
