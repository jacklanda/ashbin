import sys, time
from functools import lru_cache

sys.setrecursionlimit(99999)
''' import time

def factorial(num):
    recurse = lambda x: 1 if x == 1 else x*factorial(x-1)
    return recurse(num)

if __name__ == "__main__":
    while(1):
        num = input("输入一个正整数：")
        start = time.perf_counter()
        print(num, "的阶乘为：", factorial(int(num)))
        end = time.perf_counter()
        print(f"{num}层递归需时：{end - start}秒")
        print("") '''

@lru_cache(maxsize=1024)
def feb(i: int):
    if(i == 0):
        return i
    if(i == 1):
        return 2
    return feb(i-2) + feb(i-1)

while(1):
    start = time.perf_counter()
    num = input("Please input a number to calculate: ")
    print(feb(int(num)))
    end = time.perf_counter()
    print(f"continued time: {end - start}s")
    print("")
