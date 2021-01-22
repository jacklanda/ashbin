from re import *

from pattern import collection

def test():
    raw_text = "#reg{ font-family:\"宋体\",Arial; font-size:12px;background:#fff;} .head_pub{width:978px;display:block;border:1px #EEE solid; background:#f2f2f2;height:28px; font-size:12px; line-height:28px;margin:2px auto 0;"
    pattern = collection.pattern("css")
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
