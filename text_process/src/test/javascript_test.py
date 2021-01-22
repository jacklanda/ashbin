import warnings
from re import *

from pattern import collection

warnings.filterwarnings("ignore")

def test():
    raw_text = "通化辉南县经济适用房_通化辉南县经适房_通化辉南县经济适用房转让_通化去114网通化切换城市var googlequerykey ='二手经适房 二手房买卖 二手房地产公司' ;                                                                                   var AdKeyWords = 'jingshifang';var cityname ='通化' ; var ChildURL =  'ershoufang';不限出售求购不限东昌区二道江区梅河口市集安市通化县辉南县柳河县其他不限一室两室三室四室四室以上不限毛坯简单中档精装豪华不限个人经纪人免费发布二手房信息»"
    pattern = collection.pattern_test("js_var")
    print(f"匹配模式为：{pattern}")
    print("----------------------------------------------")
    #return_text = findall(pattern, raw_text)
    pattern = compile(pattern)
    return_text = sub(pattern, "替换成功", raw_text)
    print(return_text)

    ''' if(return_text):
        for i, each in enumerate(return_text):
            print(f"第{i+1}个匹配结果：{each}")
    else:
        print("Not Found pattern-like string!") '''

if __name__ == "__main__":
    test()
