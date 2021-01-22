import redis
import httpx
import asyncio_redis
import aioredis

import asyncio, time

proxies = {
        "http": "http://127.0.0.1:8889",
        "https": "https://127.0.0.1:8889"
        }

cookies = {
    '__cfduid': 'd78de13ac3e25c18c97656cd57fc4c8901608608103',
    'country_code': 'FR',
    'geocode': '115764',
    'geolevel1': '73072',
    'geolevel2': '83093',
    'geolevel3': '83165',
    'geolevel4': '115755',
    '_ga': 'GA1.2.1767339306.1608608115',
    '_gid': 'GA1.2.1308653579.1608608115',
    '_ttuu.s': '1608620922332',
    'tt.u': '0100007F6D69E15F5D06828002898915',
    '_fbp': 'fb.1.1608608321666.1045875150',
    'tt.nprf': '',
    '__gads': 'ID=53f4a7888142e5c5-22bb1a5b8fa6009c:T=1608608321:S=ALNI_MZZs9hBkNxVp-FmOGn21oZ3eJCn3w',
    'nvg55810': 'd2e139b210e6bdb476d9928c209|0_358',
    '_tli': '5800303711360425779',
    '_tlc': 'www.adorocinema.com%2Fnoticias-materias-especiais%2F:1608620888:www.adorocinema.com%2Fnoticias-materias-especiais%2F%3Fpage%3D2:adorocinema.com',
    '_tlv': '2.1608608315.1608609049.1608620888.5.4.1',
    '_tlp': '1186:6458737',
    'cto_bundle': 'G8NewV9xMFBjb3pvcDlreTNqJTJCeHJRREE4WSUyRjE2UFdRVXRocW1HTTd0RVFKdkFyeGw2aktpVDRZaTZURnBqSTFxMklOZmdSWmVlNzk1bUJsbkJyZWU4WFgzQVpjTEVPc1hPVEZ4dkhtd1R6eHB6UGQxZ2lxVFhwOXplWXFGZDllaFhYc3laRVBxdlpucm5rVnR5Rlk0aCUyRnlmWnclM0QlM0Q',
    'ACCOK': 'true',
    'trc_cookie_storage': 'taboola%2520global%253Auser-id%3D9b86db8b-d1ef-4473-9b91-c84dcddc10ba-tuct6daf296',
    '_tb_sess_r': 'http%3A//www.adorocinema.com/noticias-materias-especiais/%3Fpage%3D2',
    '_tb_t_ppg': 'http%3A//www.adorocinema.com/noticias/filmes/noticia-156882/',
    'tt_c_vmt': '1608620872',
    'tt_c_c': 'direct',
    'tt_c_s': 'direct',
    'tt_c_m': 'direct',
    '_ttdmp': '|LS:|CA:CA10265,CA17145,CA18488,CA5211,CA12931',
    '_tls': '*.768845,768847,768846..0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

async def request(client, pn):
    try:
        r = await client.get(f"http://www.adorocinema.com/noticias-materias-especiais/?page={str(pn)}", headers=headers, cookies=cookies, timeout=60)
    except Exception as e:
        r = "None"
        print("网站请求错误：", end="")
        print(e)
    #print(r.content.decode("utf-8"))
    print(f"已爬取第{pn}页...")
    try:
        await redis_lpush(r.content.decode("utf-8"))
    except Exception as e:
        print("Redis插入失败", end="")
        print(e)
        pass

async def request_monster(client, url):
    try:
        r = await client.get("http://www.adorocinema.com" + url, headers=headers, cookies=cookies, timeout=60)
    except Exception as e:
        r = "None"
        print("网站请求错误：", end="")
        print(e)
    print(f"已爬取 {'http://www.adorocinema.com' + url}...")
    try:
        await redis_seq_lpush(r.content.decode("utf-8"))
    except Exception as e:
        print("Redis插入失败", end="")
        print(e)
        pass


async def parser(raw_html):
    xpath = "//a/@href"

async def redis_lpush(raw_html):
    client = await aioredis.create_redis_pool("redis://127.0.0.1")
    await client.lpush("ADOROCINEMA_PAGE_HTML_SEQ", raw_html)
    client.close()
    await client.wait_closed()

async def redis_seq_lpush(raw_html):
    client = await aioredis.create_redis_pool("redis://127.0.0.1")
    await client.lpush("ADOROCINEMA_SEQ_SEQ", raw_html)
    client.close()
    await client.wait_closed()

def redis_rpop(client):
    return client.rpop("ADOROCINEMA_URL_SEQ").decode()

async def main():
    async with httpx.AsyncClient() as client:
        client.proxies = proxies
        start = time.perf_counter()
        task_list = []
        for pn in range(2810):
            req = request(client, pn+1)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)
        end = time.perf_counter()
    print(f"累计发送2810个请求，共花费：{end-start}秒")

async def monster():
    async with httpx.AsyncClient() as client:
        client.proxies = proxies
        start =time.perf_counter()
        task_list = []
        r_client = await asyncio_redis.Pool.create(host="127.0.0.1", port=6379)
        url = await r_client.rpop("ADOROCINEMA_URL_SEQ")
        count = 1
        while(url):
            req = request_monster(client, url)
            task = asyncio.create_task(req)
            task_list.append(task)
            url = await r_client.rpop("ADOROCINEMA_URL_SEQ")
            count += 1
        await asyncio.gather(*task_list)
        end = time.perf_counter()
    print(f"累计发送{count}个请求，共花费：{end-start}秒")


if __name__ == "__main__":
    import url_extract
    # asyncio.run(main())
    url_extract.extract("")
    asyncio.run(monster())
