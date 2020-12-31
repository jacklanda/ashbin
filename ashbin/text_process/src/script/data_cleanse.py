#-*- coding: UTF-8 -*-

import re, os, time, warnings
from multiprocessing import Pool

from script.langconv import *
from script.cn_tn import *
from pattern import collection

import timeout_decorator
from timeout import timeout

RAW_DIR_PATH = "../input/"
OUTPUT_DIR_PATH = "../output/"
TXT_NAME_LIST = os.listdir(RAW_DIR_PATH)


def controller(cpu_core_nums):
    with Pool(processes = cpu_core_nums) as pool:
        pool.map(cleanse, TXT_NAME_LIST)

# @profile
def cleanse(txt_name):
    start_time = time.time()
    warnings.filterwarnings("ignore")
    #eventlet.monkey_patch()
    raw = read_raw(txt_name)
    processed = text_match(raw)
    text_save(processed, txt_name)             # 当所有模式匹配结束后，将结果存储至新的txt文件中
    end_time = time.time()
    print(f"\n共耗时{end_time - start_time}秒")

def read_raw(txt_name):
    try:
        with open(raw_path(txt_name), "r") as f:
            for line in f:
                yield line
    except Exception as e:
        print("文本打开错误，原因如下：")

def raw_path(txt_name):
    return RAW_DIR_PATH + txt_name

def save_path(txt_name):
    return OUTPUT_DIR_PATH + "processed_" + txt_name

''' 预编译正则表达式 '''
def compile_regex(matcher):
    return re.compile(matcher)

def text_match(raw):
    patterns = collection.pattern()                  # 返回一个包含各种正则模式的哈希
    old_list = raw
    time_limit = 3
    for i, key in enumerate(patterns.keys()):        # 对哈希的键进行带索引遍历
        count = 0
        if(i != 0):
            old_list = new_list
        new_list = []                                # 用于存放匹配替换后的行对象
        pattern = compile_regex(patterns[key])
        print(f"\n*****************正在匹配含有「{key}」的行*****************")
        for line in old_list:                        # 从上一次匹配结束后的list对象中取行对象
            try:
                if(key == "single_punctuation" or key == "single_punc" or key == "except_punc"):
                    line = sub_every_line(pattern, " ", line)  # 对于标点符号，使用一个空格符替换
                else:
                    line = sub_every_line(pattern, "", line)   # 对于其他文本，使用空串替换
            except Exception as e:
                line = ""
                print(e)
            line = punc2zh(line)
            line = NSWNormalizer(line).normalize()   # 将各种形式的阿拉伯数字转换为简中数字
            line = translateToSimpleCH(line)
            line = line.lower()                      # 将所有英文字母置换为小写
            #line = strH2F(line)
            count += 1
            print(f"当前模式：{patterns[key]}，已处理第「{count}」行")
            if(line == "\n"):                        # 如果为空行，则略去
                pass
            elif(line[-1] == "\n"):
                new_list.append(line)
            else:                                    # 如果非空行，压入new_list中，供下一轮模式匹配
                new_list.append(line + "\n")
        print(f"*****************模式「{key}」匹配完成*****************")
    print("\n***********************文本清洗完毕～***********************\n")
    return new_list

@timeout_decorator.timeout(3)
def sub_every_line(pattern, sub_content, line):
    line = re.sub(pattern, sub_content, line)
    return line

def translateToSimpleCH(content):
    """
    将繁体转换为简体
    """
    content = Converter('zh-hans').convert(content)
    #content = content.encode('utf-8')
    return content

def strH2F(strContent):
    """
    半角字符转全角
    """
    rstring = ""
    #首先将输入串转换成unicode
    temp = strContent#str(strContent, "utf-8")
    for uchar in temp:
        inside_code = ord(uchar)
        #空格需另外处理
        if inside_code==0x0020:
            #inside_code=0x3000
            inside_code=0x0020
        #其他符号是顺序编码
        else:
            if inside_code<0x0020 or inside_code>0x7e: #不是半角字符返回原来的字符
                rstring += uchar
                continue
            else:
                inside_code+=0xfee0
        rstring += chr(inside_code);
    #rstring = rstring.encode("utf-8");
    return rstring;

def punc2zh(line):
    pattern_list = collection.punc2zh()
    for i, pattern in enumerate(pattern_list):
        matchers = re.findall(pattern, line)
        if(i == 0):
            if matchers:
                for matcher in matchers:
                    word = matcher[0].replace('-', '到', 1)
                    line = line.replace(matcher[0], word, 1)
        elif(i == 1):
            if matchers:
                for matcher in matchers:
                    word = matcher[0].replace(".", "点", 1)
                    line = line.replace(matcher[0], word, 1)
    return line

def text_save(lines, save_name):
    try:
        with open(save_path(save_name), "a") as f:
            for line in lines:
                f.write(line)
        print("***********************文本存储完毕～***********************")
    except Exception as e:
        print("文本存储错误，原因如下：")
        print(e)

if __name__ == "__main__":
    cleanse()
