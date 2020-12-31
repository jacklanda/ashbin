# -*- coding: UTF-8 -*-
from concurrent.futures import as_completed
import os
import sys
import requests
import time
import pymongo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
from tool import crawler_ip
from tool.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor

from tool.mail import mail

connect = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(connect)
db = client['proxies']
test_collection = db['proxies_test'] #待测
collection = db['proxies'] #正确


def daili():
    urls=[
        # 'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=11&pack=103875&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4',
        'http://http.tiqu.alicdns.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=11&pack=103879&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
    ]
    for url in urls:
        try:
            response=requests.get(url)
            html=response.json()
            if html['code']==111:
                time.sleep(10)
            if html['code']==0 or html['success'] ==True or html['msg']=='0':
                data=html['data']
                for proxyHost in data:
                    try:
                        ip=proxyHost['ip']
                        port=proxyHost['port']
                        proxy = 'http://' + str(ip)+':'+str(port)
                        if collection.find_one({'_id': proxy}):
                            collection.delete_one({'_id': proxy})
                        collection.insert_one({'_id': proxy, 'type': 0, 'score': 100})
                        print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入成功', proxy)
                    except Exception as e:
                        print(444444,e)
                return data
        except Exception as e:
            print(222222,e)


def delete_proxy(query=None):
    if query:
        try:
            if test_collection.find_one(query):
                test_collection.delete_one(query)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除成功', query)
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除失败', query, e)


def find_proxy(query=None):
    try:
        document = collection.find_one(query, sort=[('score', -1)])
        return document
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '查找失败', query, e)


def find_proxies(query=None, id=None, page=0, sort_query=None):
    if sort_query is None:
        sort_query = [("_id", 1)]
    if id:
        for document in collection.find({'_id': {'$gt': id}}).sort(sort_query).limit(1):
            return document
    else:
        for document in collection.find(query).sort(sort_query).limit(1).skip(page):
            return document


def alter_proxy(query=None):
    try:
        proxy = collection.find_one(query)
        if proxy:
            score = {"$set": {"score": 50}}
            collection.update(query, score)
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '修改失败', query, e)


def update_proxy(query=None):
    try:
        proxy = collection.find_one(query)
        if proxy:
            try:
                score = {"$set": {"score": proxy['score'] - 1}}
            except:
                score = {"$set": {"score": 50}}
            collection.update(query, score)
            if proxy['score'] <= 1:
                collection.delete_one(query)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除成功', query)
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除失败', query, e)


def test(proxy):
    proxies = {
        'http': proxy,
        'https': proxy
    }
    try:
        url = 'http://www.httpbin.org/ip'
        response = requests.get(url, proxies=proxies, timeout=60)
        # 0代表高隐
        if collection.find_one({'_id': proxy}):
            collection.delete_one({'_id': proxy})
        if ',' in response.text:
            collection.insert_one({'_id': proxy, 'type': 1, 'score': 50})
        else:
            collection.insert_one({'_id': proxy, 'type': 0, 'score': 50})
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入成功', proxy)
    except:
        query = {'_id': proxy}
        delete_proxy(query)


def run():
    with BoundedThreadPoolExecutor(max_workers=40) as t:
        proxy = crawler_ip.find_proxies()
        while proxy:
            try:
                task = t.submit(test, proxy['_id'])
                as_completed(task, timeout=60)
            except:
                pass
            proxy = crawler_ip.find_proxies(id=proxy['_id'])
    print('proxy 空')
    time.sleep(300)
    # ret = mail('test_ip', 'test_proxies为空')
    # if ret:
    #     print("邮件发送成功")
    # else:
    #     print("邮件发送失败")


if __name__ == '__main__':
    # schedule.every().seconds.do(run)
    while True:
        #     schedule.run_pending()
        run()
