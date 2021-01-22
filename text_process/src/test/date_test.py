from re import *

from pattern import collection

def test():
    raw_text = "美图GIF免费无病毒无插件无暗扣推荐等级：更新日期：2012-1-16总下载量：233611软件介绍“美图GIF”是一款简专辑上传时间: 2009年5月5日"
    pattern = collection.pattern("date")
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
