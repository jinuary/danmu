import json

import requests


def request_url(url, headers=None):
    if headers is None:
        headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            # "Cache-Control": "max-age=0",
            # "Connection": "keep-alive",
            # "Sec-Fetch-Dest": "document",
            # "Sec-Fetch-Mode": "navigate",
            # "Sec-Fetch-Site": "none",
            # "Sec-Fetch-User": "?1",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "referer": 'https://www.mgtv.com/',
            # "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": "Windows",
            # "Accept-Encoding": "gzip, deflate, br"
        }

    response = requests.request("GET", url, headers=headers)

    return response.content


def request_url_json(url, headers):
    response = request_url(url, headers)
    return json.loads(response)


def request_post_json(url, payload, headers, querystring=None):
    response = requests.request("POST", url, json=payload, headers=headers, params=querystring).content
    # response = requests.post(url, headers=headers, json=json_data).content
    return json.loads(response)
