import requests


def request_package(method='get', url=None, headers=None, proxies=None, data=None, cookies=None):
    if method == 'get':
        response = requests.get(url=url, headers=headers, proxies=proxies, cookies=cookies)
        return response
    else:
        response = requests.post(url=url, headers=headers, proxies=proxies, data=data, cookies=cookies)
        return response
