from multiprocessing import Pool

import redis
from lxml import html

def html_rpop(client):
    return client.rpop("ADOROCINEMA_PAGE_HTML_SEQ")

def url_lpush(client, url_list):
    return client.lpush("ADOROCINEMA_URL_SEQ", *url_list)

def extract(status):
    client = redis.Redis(host="127.0.0.1", port=6379)
    xpath_rule = "//a/@href"
    raw_html = html_rpop(client)
    while(raw_html):
        try:
            dom_tree = html.fromstring(raw_html)
            url_list = dom_tree.xpath(xpath_rule)
        except Exception as e:
            print("XPATH解析错误！")
            print(e)
            continue
        url_lpush(client, url_list)
        raw_html = html_rpop(client)
    return

if __name__ == "__main__":
    pool = Pool(4)
    pool.map(extract, "我没参数呀！")
