# -*- coding: UTF-8 -*-
from lxml import etree
import os
import sys
import re
import requests
import time
import pymongo
import queue
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
from tool.user_agent import User_Agent
from tool import test_ip
from tool.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor


connect = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(connect)
db = client['proxies']
test_collection = db['proxies_test']


def get_method(url):
    i = 0
    while i < 3:
        ua = User_Agent()
        headers = {'User-Agent': ua.random()}
        proxy = test_ip.find_proxy()
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), url)
            if proxy:
                proxy = proxy['_id']
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
                response = requests.get(url=url, headers=headers, proxies=proxies, timeout=100)
                if response.status_code == 503:
                    raise Exception('状态码503')
                proxy = {'_id':proxy}
                test_ip.alter_proxy(proxy)
            else:
                response = requests.get(url=url, headers=headers, timeout=100)
                if response.status_code == 503:
                    time.sleep(300)
                    raise Exception('状态码503')
            return response
        except Exception as e:
            i = i + 1
            if proxy:
                query = {'_id': proxy}
                test_ip.update_proxy(query)
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '超时', url, e)
    raise Exception('已经达到最大重试，url', url)


def save_proxy(proxy):
    if proxy:
        proxy = {
            '_id': 'http://' + proxy
        }
        try:
            if test_collection.find_one(proxy):
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '已经存在', proxy)
            else:
                test_collection.insert_one(proxy)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入成功', proxy)
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入失败', proxy, e)


def find_proxies(query=None, id=None, page=0, sort_query=None):
    if sort_query is None:
        sort_query = [("_id", 1)]
    if id:
        for document in test_collection.find({'_id': {'$gt': id}}).sort(sort_query).limit(1):
            return document
    else:
        for document in test_collection.find(query).sort(sort_query).limit(1).skip(page):
            return document


def ip89():
    url = 'http://www.89ip.cn/api.html'
    try:
        response = get_method(url)
        html = etree.HTML(response.text)
        num = html.xpath('//*[@class="fly-panel fly-list-one"]/dd[1]/text()')
        if num:
            num = re.findall('\d+', num[0])[0]
        else:
            return
        url = 'http://www.89ip.cn/tqdl.html?api=1&num={}'
        url = url.format(num)
        response = get_method(url)
        proxies = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', response.text)
        proxies = set(proxies)
        return proxies
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '89ip,url', url, e)


def proxylistdaily():
    url = 'https://www.proxylistdaily.net/'
    try:
        response = get_method(url)
        proxies = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', response.text)
        proxies = set(proxies)
        return proxies
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'proxylistdaily,url', url, e)


def ip66():
    url = 'http://www.66ip.cn/pt.html'
    try:
        response = get_method(url)
        html = etree.HTML(response.text)
        num = html.xpath('//span/strong/text()')
        if num:
            num = re.findall('\d+', num[0])[0]
        else:
            return
        http_url = 'http://www.66ip.cn/mo.php?tqsl={}'
        anonymous_url = 'http://www.66ip.cn/nmtq.php?getnum={}'
        urls = [http_url, anonymous_url]
        proxies = set()
        for url in urls:
            url = url.format(num)
            response = get_method(url)
            proxies_temp = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', response.text)
            proxies.update(proxies_temp)
        return proxies
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '66ip,url', url, e)


def get_proxies():
    proxies_ip66 = ip66()
    proxies_ip89 = ip89()
    proxy_list_daily = proxylistdaily()
    proxies = proxies_ip66 | proxies_ip89 | proxy_list_daily
    # proxies = proxies_ip89 | proxy_list_daily
    if proxies:
        for proxy in proxies:
            save_proxy(proxy)


def yip7():
    base_url = 'https://www.7yip.cn/free/'
    next_url = '?action=china&page=1'
    next_url = base_url + next_url
    while next_url:
        try:
            old_url = next_url
            item = get_yip7(next_url)
            if item:
                proxies, next_url = item[0], item[1]
                yield proxies
            if old_url == next_url:
                break
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '7yip,url', next_url, e)
            break


def get_yip7(next_url):
    base_url = 'https://www.7yip.cn/free/'
    try:
        response = get_method(next_url)
        html = etree.HTML(response.text)
        trs = html.xpath('//tbody/tr')
        next_url = html.xpath('//a[@aria-label="Next"]/@href')
        proxies = set()
        for tr in trs:
            try:
                ip = tr.xpath('./td[@data-title="IP"]/text()')
                port = tr.xpath('./td[@data-title="PORT"]/text()')
                proxy = ip[0] + ':' + port[0]
                proxies.add(proxy)
            except:
                continue
        if proxies:
            if next_url:
                next_url = next_url[0]
                return proxies, base_url + next_url
            else:
                return proxies, None
        else:
            if next_url:
                next_url = next_url[0]
                return None, base_url + next_url
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '7yip,url', next_url, e)
        raise e


def save_7yip():
    for proxies in yip7():
        if proxies:
            for proxy in proxies:
                save_proxy(proxy)


def get_ihuan(url):
    ua = User_Agent()
    headers = {'User-Agent': ua.random()}
    print(time.strftime('%Y-%m-%d %H:%M:%S'), url)
    proxy = test_ip.find_proxy({'type': 0})
    try:
        if proxy:
            proxy = proxy['_id']
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(url, headers=headers, proxies=proxies, timeout=60)
            proxy = {'_id': proxy}
            test_ip.alter_proxy(proxy)
        else:
            response = requests.get(url, headers=headers, timeout=60)
        html = etree.HTML(response.text)
        trs = html.xpath('//tbody/tr')
        next_url = html.xpath('//a[@aria-label="Next"]/@href')
        if next_url:
            next_url = next_url[0]
        proxies = set()
        for tr in trs:
            try:
                ip = tr.xpath('./td[1]/a/text()')
                port = tr.xpath('./td[2]/text()')
                if ip and port:
                    proxy = ip[0] + ':' + port[0]
                    proxies.add(proxy)
            except:
                continue
        return proxies, next_url
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'ihuan,url', url, e)
        if proxy:
            query = {'_id': proxy}
            test_ip.update_proxy(query)


def ihuan():
    home_url = 'https://ip.ihuan.me/'
    next_url = home_url
    while next_url:
        try:
            result = get_ihuan(next_url)
            if result:
                proxies, next_url = result
                if next_url:
                    next_url = home_url + next_url
                yield proxies
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'ihuan,url', next_url, e)
            break


def save_ihuan():
    for proxies in ihuan():
        if proxies:
            for proxy in proxies:
                save_proxy(proxy)


def get_kuaidaili(url):
    try:
        response = get_method(url)
        html = etree.HTML(response.text)
        trs = html.xpath('//tbody/tr')
        num = html.xpath('//*[@id="listnav"]/ul/li[last()-1]/a/text()')
        proxies = set()
        for tr in trs:
            ip = tr.xpath('./td[@data-title="IP"]/text()')
            port = tr.xpath('./td[@data-title="PORT"]/text()')
            proxy = ip[0] + ':' + port[0]
            proxies.add(proxy)
        if proxies:
            if num:
                num = int(num[0])
                return proxies, num
            else:
                return proxies, None
        else:
            if num:
                num = int(num[0])
                return None, num
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'kuaidaili,url', url, e)


def save_kuaidaili(base_url):
    url = base_url.format(1)
    num = 0
    result = get_kuaidaili(url)
    if result:
        proxies, num = result[0], result[1]
        if proxies:
            for proxy in proxies:
                save_proxy(proxy)
    if num:
        page = 2
        while page < num:
            with BoundedThreadPoolExecutor(max_workers=100) as executor:
                executor.submit(kuaidaili,base_url,page)
                page = page + 1


def kuaidaili(base_url,page):
    # base_url = {
    #     'https://www.kuaidaili.com/free/inha/{}/',
    #     'https://www.kuaidaili.com/free/intr/{}/',
    # }
    # for url in base_url:
    #     save_kuaidaili(url)
    url = base_url.format(page)
    result = get_kuaidaili(url)
    if result:
        proxies, num = result[0], result[1]
        if proxies:
            for proxy in proxies:
                save_proxy(proxy)
        if num < page:
            raise


def get_xicidaili(url):
    home_url = 'https://www.xicidaili.com'
    try:
        response = get_method(url)
        if response.status_code == 503:
            print('xicidaili暂时封杀')
        html = etree.HTML(response.text)
        trs = html.xpath('//table//tr[position()>1]')
        proxies = set()
        next_url = html.xpath('//a[@class="next_page"]/@href')
        if next_url:
            next_url = home_url + next_url[0]
        else:
            next_url = None
        for tr in trs:
            ip = tr.xpath('./td[2]/text()')
            port = tr.xpath('./td[3]/text()')
            proxy = ip[0] + ':' + port[0]
            proxies.add(proxy)
        return proxies, next_url
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'xicidaili,url', url, e)


def save_xicidaili(next_url):
    try:
        while next_url:
            old_url = next_url
            result = get_xicidaili(next_url)
            if result:
                proxies, next_url = result[0], result[1]
                if proxies:
                    for proxy in proxies:
                        save_proxy(proxy)
            if next_url == old_url:
                break
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'xicidaili,url', next_url, e)


def xicidaili():
    base_url = {
        'https://www.xicidaili.com/nn/',
        'https://www.xicidaili.com/nt/',
        'https://www.xicidaili.com/wn/',
        'https://www.xicidaili.com/wt/',
    }
    for url in base_url:
        save_xicidaili(url)


def run():
    with BoundedThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(get_proxies)
            executor.submit(save_7yip)
            executor.submit(save_ihuan)

            xicidaili_urls = {
                'https://www.xicidaili.com/nn/',
                'https://www.xicidaili.com/nt/',
                'https://www.xicidaili.com/wn/',
                'https://www.xicidaili.com/wt/',
            }
            for url in xicidaili_urls:
                executor.submit(save_xicidaili, url)

            kuaidaili_urls = {
                'https://www.kuaidaili.com/free/inha/{}/',
                'https://www.kuaidaili.com/free/intr/{}/',
            }
            for url in kuaidaili_urls:
                executor.submit(save_kuaidaili, url)


if __name__ == '__main__':
    # schedule.every().seconds.do(run)
    while True:
        #     schedule.run_pending()
        run()
