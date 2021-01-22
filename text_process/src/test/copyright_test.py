from re import *

from pattern import collection

def test():
    raw_text = "DKP分值增加Copyright 2000-2008 DuoWan.com [多玩游戏]ICP证编号：粤B2-20050785【海阳技工/工人招聘|海阳最新招聘技工/工人信息】 - 烟台赶集网"
    pattern = collection.pattern("copyright")
    print(f"匹配模式为：{pattern}")
    print("----------------------------------------------")
    return_text = findall(pattern, raw_text)

    if(return_text):
        for i, each in enumerate(return_text):
            print(f"第{i}个匹配结果：{each}")
    else:
        print("Not Found pattern-like string!")

if __name__ == "__main__":
    test()
