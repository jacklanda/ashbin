#!/usr/bin/python3

import requests
import redis  # 导入redis 模块
import os
import sys
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)

from tool.user_agent import User_Agent
pool = redis.ConnectionPool(host='localhost',port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def test_word(word):
    if r.sismember("set1", word):  # word是不是集合的成员
        return True
    if r.hget("hash1", word) == word:
        return True
    else:
        ua = User_Agent()
        headers = {'User-Agent': ua.random()}
        url = 'http://www.youdao.com/w/{}/'.format(word)
        try:
            response = requests.get(url, headers=headers, timeout=300)
            if 'error-wrapper' in response.text:
                return False
            if '您要找的是不是' in response.text:
                return False
            if '添加释义' in response.text:
                return False
            if 'baav' not in response.text:
                return False
            else:
                # pipe = r.pipeline(transaction=False)    # 默认的情况下，管道里执行的命令可以保证执行的原子性，执行pipe = r.pipeline(transaction=False)可以禁用这一特性。
                # pipe = r.pipeline(transaction=True)
                pipe = r.pipeline()  # 创建一个管道
                # pipe.sadd("dict", word)  # 往集合中添加元素
                pipe.hset("hash1", word, '1')
                pipe.execute()
                return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    pass
    # print(test_word('CEO'))
    # print(r.scard("dict"))  # 集合的长度是4
    # print(r.smembers("dict"))  # 获取集合中所有的成员
    # print(r.keys())  # 查询所有的Key
    # print(r.dbsize())  # 当前redis包含多少条数据
    # r.save()    # 执行"检查点"操作，将数据写回磁盘。保存时阻塞
    # r.flushdb()        # 清空r中的所有数据
    # for word in r.smembers("dict"):
    #     r.hset("hash1", word, word)
        # print(test_word(word))
    # r.delete('dict')
    # print(r.exists('dict'))
    # print(r.keys())
    # a=r.hgetall("hash1")
    # # print(r.hkeys("hash1"))
    # print(type(a))
    # print(r.hlen('hash1'))



    # file = r'C:\Users\18291\PycharmProjects\crawler\tool\dict.txt'
    # with open(file, 'w', encoding='utf-8') as f:
    #     str_dict = r.hgetall('hash1')
    #     str_dict = json.dumps(str_dict)
    #     f.write(str_dict)
