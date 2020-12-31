#!/bin/env python
#encoding=utf-8

"""
默认第一列为key，其他列为文本内容，只对文本内容进行预处理
注意：输入文件为gb18030格式
"""

import os, sys
import re
from langconv import *

def UTF8ToGB18030(input_file, output_file):
    res = os.system('iconv -f utf-8 -t gb18030 ' + input_file + ' -o ' + output_file  + ' 1>/dev/null 2>/dev/null')
    return res

def GB18030ToUTF8(input_file, output_file):
    res = os.system('iconv -f gb18030 -t utf-8 ' + input_file + ' -o ' + output_file  + ' 1>/dev/null 2>/dev/null')
    return res

def removePunc(line):
    """
    去除标点符号
    """
    delCStr = '＇｛｝［］＼｜｀～＠＃＄％＾＆＊（）＿＋，。、‘’“”《》？：；【】——~！@￥%……&（）,.?<>:;\[\]|`\!@#$%^&()+?\'\"/_'.decode("utf-8")
    line = line.decode("utf-8")
    new_line = re.sub('[%s]' % delCStr, '', line)
    new_line = new_line.encode("utf-8")
    return new_line

def delSymbol(strContent):
    '''
    删除符号，只保留中文、英文字符以及数字。需在全角转半角之后运行
    #如果句子中只包含英文字符，则返回空(暂不加入)
    '''
    rstring = ""
    temp = unicode(strContent, "utf-8")
    all_english = True
    for uchar in temp:
        inside_code = ord(uchar)

        if inside_code >= 48 and inside_code <= 57: #数字
            rstring += uchar
            all_english = False
        elif inside_code >= 65 and inside_code <=90:#大写英文字母
            rstring += uchar
        elif inside_code  >= 97 and inside_code <= 122:#小写英文字母
            rstring += uchar
        elif inside_code >= 0x4e00 and inside_code <= 0x9fa5:#中文
            rstring += uchar
            all_english = False
        else:
            rstring  += ""
    rstring = rstring.encode("utf-8")

    """
    if all_english:
        rstring = ""
    """
    return rstring

def strH2F(strContent):
    """
    半角字符转全角
    """
    rstring = ""
    #首先将输入串转换成unicode
    temp = unicode(strContent, "utf-8")
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
        rstring += unichr(inside_code);
    rstring = rstring.encode("utf-8");
    return rstring;

def strF2H(strContent):
    """
    全角字符转半角
    """
    rstring = ""
    #首先将输入串转换成unicode
    temp = unicode(strContent, "utf-8")
    for uchar in temp:
        inside_code = ord(uchar)
        #空格需另外处理
        if inside_code==0x3000:
            inside_code=0x0020
        #其他全角符号是顺序编码
        else:
            inside_code-=0xfee0
            if inside_code<0x0020 or inside_code>0x7e: #转完之后不是半角字符返回原来的字符
                rstring += uchar
                continue
        rstring += unichr(inside_code);
    rstring = rstring.encode("utf-8");
    return rstring;

def translateToSimpleCH(content):
    """
    将繁体转换为简体
    """
    content = Converter('zh-hans').convert(content.decode('utf-8'))
    content = content.encode('utf-8')
    return content

def translateToComplexCH(content):
    """
    将简体转换为繁体
    """
    content = Converter('zh-hant').convert(line.decode('utf-8'))
    content = content.encode('utf-8')
    return content

def main():
    if len(sys.argv) != 3:
        print "Usage: %s input output" % sys.argv[0]
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]

    #转换为utf-8编码
    #input_utf8 = input+'.utf8'
    #GB18030ToUTF8(input, input_utf8)

    data = open(input).readlines()
    #ferr = open("err.key", "w")
    new_data = []
    for line in data:
        content = line.strip()
        #全角转半角后去除标点符号
        #content = strF2H(content)
        #content = delSymbol(content)
        #if content == "":
        #    ferr.write(key + "\n")
        #    continue
        #英文字母转换为大写
        #content = content.upper()
        #英文字母转换为小写
        content = content.lower()
        #半角转全角
        ''' content = strH2F(content) '''
        #繁体转简体
        content = translateToSimpleCH(content)

        new_data.append("%s\n" % content)

    with open(output, "w") as fw:
        for line in new_data:
            fw.write(line)


if __name__ == "__main__":
    main()
