import json
import re
import time
import os
import sys
from lxml import etree
from multidict import CIMultiDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from tool.num_to_chinese import num_chinese, num_year,dao
from tool.harvesttext import NSWNormalizer
from tool.langconv import Converter
from tool.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor

# file = r'C:\Users\18291\PycharmProjects\crawler\tool\dict.txt'
file = r'/data/wangjie/corpus/TN/tool/dict.txt'
with open(file, 'r', encoding='utf-8') as f:
    str_dict = f.read()
str_dict = json.loads(str_dict)
str_dict = CIMultiDict(str_dict)



def split_txt(path,save_path):
    j = 1
    with open(path, 'r', encoding='utf-8') as f:
        with BoundedThreadPoolExecutor(max_workers=100) as t:
            while True:
                data = f.readlines(1024 * 1024)
                if data:
                    t.submit(save_txt, data, j,save_path)
                else:
                    break
                j = j + 1


def save_txt(data, j,save_path):
    file_name = save_path+r'\part{}'.format(j) + '.txt'
    with open(file_name, 'w', encoding='utf-8') as f2:
        for line in data:
            line = json.loads(line)
            keywords = line.get('keywords')
            keywords = re.sub('\n|\r', '', keywords)
            f2.write(keywords + '\n')

            desc = line.get('desc')
            desc = re.sub('\n|\r', '', desc)
            f2.write(desc + '\n')

            title = line.get('title')
            title = re.sub('\n|\r', '', title)
            f2.write(title + '\n')

            content = line.get('content')
            content = re.sub('\n|\r', '', content)
            f2.write(content + '\n')
    print(file_name)

def clean(root, name):
    if not root or not name:
        return
    #if len(name.split('.')) != 2:
    #    return
    try:
        file = os.path.join(root, name)
        text = ''
        lines = []
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if lines:
            for i, line in enumerate(lines):
                try:
                    if i % 1000 == 0:
                        print(time.strftime('%Y-%m-%d %H:%M:%S') + '\t' + file + '\t行:' + str(i))
                    # if line:
                    #     try:
                    #         line = json.loads(line)
                    #         line = line['text']
                    #     except:
                    #         pass
                    # else:
                    #     lines[i] = ''
                    #     continue
                    #if line:
                    #    try:
                    #        # line = etree.HTML(line)
                    #        # line = line.xpath('string(.)')
                    #        line = etree.HTML(line).xpath('string(.)')
                    #    except:
                    #        pass
                    #else:
                    #    lines[i] = ''
                    #    continue
                    if line:
                        line = str(line)
                        line = Converter('zh-hans').convert(line)
                    else:
                        lines[i] = ''
                        continue
                    if line:
                        line.encode('utf-8')
                    else:
                        lines[i] = ''
                        continue
                    # if line:
                    #     line = re.sub('//@.*?:', '', line)
                    # else:
                    #     lines[i] = ''
                    #     continue
                    # if line:
                    #     punctuation = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏."""
                    #     line = re.sub(u"([{}])+".format(punctuation), r'\1', line)
                    # else:
                    #     lines[i] = ''
                    #     continue
                    if line:
                        words = re.split('([｡。！？!?])', line)
                        if words:
                            for j, word in enumerate(words):
                                # if word:
                                #     word = re.sub('http.*?\s', '', word)
                                # else:
                                #     words[j] = ''
                                #     continue
                                # if word:
                                #     word = re.sub('回复@.*?:', '', word)
                                # else:
                                #     words[j] = ''
                                #     continue
                                # if word:
                                #     word = re.sub('\[.*?\]', '', word)
                                # else:
                                #     words[j] = ''
                                #     continue
                                if word:
                                    word = dao(word)
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    word = num_chinese(word)
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    word = num_year(word)
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    word = NSWNormalizer(word).normalize()
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    word = word.replace('°C', '摄氏度')
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    for characters in re.findall(r'[a-zA-Z-]+', word):
                                        if characters:
                                            if characters in str_dict:
                                                pass
                                            else:
                                                word = word.replace(characters, '', 1)
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    rule = re.compile(u"[^ a-zA-Z\u4e00-\u9fa5]")
                                    word = rule.sub(' ', word)
                                else:
                                    words[j] = ''
                                    continue
                                if word:
                                    string = u'零一二三四五六七八九零壹贰叁肆伍陆柒捌玖零壹貳參肆伍陸柒捌玖十百千万拾佰仟萬亿兆京垓秭穰沟涧正载億兆京垓秭穰溝澗正載十百千万拾佰仟萬'
                                    flag = 0
                                    for k in word:
                                        if k:
                                            if k in string:
                                                flag = 1
                                            else:
                                                flag = 0
                                                break
                                    if flag == 1:
                                        words[j] = ''
                                        continue
                                else:
                                    words[j] = ''
                                    continue
                                # if word:
                                #     if word == '转发微博':
                                #         words[j] = ''
                                #         continue
                                # else:
                                #     words[j] = ''
                                #     continue
                                # if word:
                                #     if word == '分享图片':
                                #         words[j] = ''
                                #         continue
                                # else:
                                #     words[j] = ''
                                #     continue
                                if word:
                                    if 1 < len(word) < 200:
                                        text = text + word + '\n'
                                words[j] = ''
                    lines[i] = ''
                except Exception as e:
                    with open('test.txt', 'a+', encoding='utf-8') as f:
                        #f.write(root + '\\' + name + '\n')
                        f.write(root + '/' + name + '\n')
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), e, '1111111路径' + root + '文件名' + name)
        file = os.path.join(root + '_after', name)
        try:
            os.mkdir(root + '_after', 0o775)
        except:
            pass
        print('aaa')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(time.strftime('%Y-%m-%d %H:%M:%S') + '\t' + file + '完成')
    except Exception as e:
        with open('test.txt', 'a+', encoding='utf-8') as f:
            # f.write(root + '\\' + name + '\n')
            f.write(root + '/' + name + '\n')
        print(time.strftime('%Y-%m-%d %H:%M:%S'), e, '22222222路径' + root + '文件名' + name)


def operationPath(path):
    # files = os.listdir(path)
    # with BoundedThreadPoolExecutor(max_workers=100) as t:
    for root, dirs, files in os.walk(path, topdown=False):
        print(root, dirs, files)
        try:
            for name in files:
                try:
                    clean(root, name)
                    # t.submit(clean, root, name)
                except:
                    pass
        except:
            pass
    exit()


if __name__ == '__main__':
    pass


    # path = r'D:\work\未完成\comment2019zh_corpus'
    # split_txt(path)
    root = sys.argv
#    split_txt(root[1],root[2])
#    operationPath(root[1])
    clean(root[1],root[2])
    exit()
    # operationPath(r'train_clue_pretrain_train_0046')
    # patth = r'D:\work\未完成\news2016zh_corpus'
    # path=r'D:\work\clean\baike_qa2019'
    # for root, dirs, files in os.walk(path, topdown=False):
    #     for name in files:
    #         print(root,name)
    # clean('train_clue_pretrain_train', 'clue_pretrain_0027550.txt')  #
    # clean('train_clue_pretrain_train', 'clue_pretrain_0027588.txt')          #
