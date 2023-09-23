import time
from concurrent.futures import ThreadPoolExecutor

def nap():
    print('Nap started...')
    time.sleep(4)
    print(3)

def main():
    print(1)
    executor = ThreadPoolExecutor(max_workers=100)
    task1 = executor.submit(nap)
    print(2)
    return 99

if __name__ == '__main__':
    data_returned_before_tasks_complete = main()
    print('data_returned_before_tasks_complete: ', data_returned_before_tasks_complete)
