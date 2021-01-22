import warnings
from re import *

from pattern import collection

warnings.filterwarnings("ignore")

def test():
    raw_text = "客:  加入 | 登入 (帳號有問題請連絡TWed2k@gmail.com) " 
    pattern = collection.pattern("email")
    print(f"匹配模式为：{pattern}")
    print("----------------------------------------------")
    return_text = findall(pattern, raw_text)

    if(return_text):
        for i, each in enumerate(return_text):
            print(f"第{i+1}个匹配结果：{each}")
    else:
        print("Not Found pattern-like string!")

if __name__ == "__main__":
    test()
