import warnings
from re import *

from pattern import collection

warnings.filterwarnings("ignore")

def test():
    raw_text = "拍摄于$4</li> <li>地址：$5</li> </ul> </div> <div class=\"userinfo\"> <a><img class=\"face beLeft\" src=\"$7\"></a> <div class=\"info beLeft\">$6"
    pattern = collection.pattern("html")
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
