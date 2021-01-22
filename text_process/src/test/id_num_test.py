import warnings
from re import *

from pattern import collection

warnings.filterwarnings("ignore")

def test():
    raw_text = "afafasdfasdf445345345fsdfg450481199911120054j"
    pattern = collection.pattern("idnum")
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
