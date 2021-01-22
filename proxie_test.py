#! /bin/python3.9
# Author: Jacklanda

import asyncio

import httpx

PROXIES = {
    "http://": "http://127.0.0.1:xxxx",
    "https://": "http://127.0.0.1:xxxx",
}


async def request(client, url):
    r = await client.get(url)
    print(r.content)


async def main(url_list):
    """
    Test httpx's http(s)-proxy implementation
    """
    async with httpx.AsyncClient(proxies=PROXIES, verify=False) as client:
        task_list = []
        for url in url_list:
            req = request(client, url)
            task = asyncio.create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)

if __name__ == "__main__":
    url_list = [
        "https://www.youtube.com",
        "https://www.google.com",
        "https://www.wikipedia.org/",
    ]
    asyncio.run(main(url_list))
