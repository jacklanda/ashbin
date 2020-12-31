import warnings
from re import *

from pattern import collection

warnings.filterwarnings("ignore")

def test():
    raw_text = "博文sunxu_65的博客http://blog.sina.com.cn/u/1153918035 [订阅][手机订阅]首页博文目录鲜橙地址： http://g.oeeee.com/104696 【复制】凤凰博报 由你开始http://blog.ifeng.com/2103852.html'<img src=http://v4.vcimg.com/images/favorite/myFavorite.gif class= onMouse  "
    pattern = collection.pattern("url")
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
