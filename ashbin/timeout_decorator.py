import time

import timeout_decorator
from timeout import timeout

def main():
    try:
        info2()
    except Exception as e:
        print(e)

    try:
        info1()
    except Exception as e:
        print(e)

    return

@timeout_decorator.timeout(3)
def info1():
    while(True):
        continue

@timeout_decorator.timeout(3)
def info2():
    time.sleep(2)
    print("info2函数未超时")
    return

main()
