import time
from datetime import date

import requests
import json

from output import encode_data,write_xml


# import pandas as pd


def request_url(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Accept-Encoding": "gzip, deflate, br"
    }

    response = requests.request("GET", url, headers=headers)

    return response.text


def get_mgtv_danmu(num1, num2, page):
    try:

        today = date.today()

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        }
        # page = 2
        url = 'https://bullet-ws.hitv.com/bullet/tx/{}/{}/{}/{}/{}/{}.json'
        print("正在爬取第" + str(page) + "页")
        danmuurl = url.format(today.year, today.month, 15, num1, num2, page)

        content = request_url(danmuurl)
        print(content)
        data = json.loads(content)
    except:
        print("无法连接")

    details = []
    for i in range(len(data['data']['items'])):  # 弹幕数据在json文件'data'的'items'中
        result = {}
        result['stype'] = num2  # 通过stype可识别期数
        result['id'] = data['data']['items'][i]['id']  # 获取id

        try:  # 尝试获取uname
            result['uname'] = data['data']['items'][i]['uname']
        except:
            result['uname'] = ''

        result['content'] = data['data']['items'][i]['content']  # 获取弹幕内容
        result['time'] = data['data']['items'][i]['time']  # 获取弹幕发布时间

        try:  # 尝试获取弹幕点赞数
            result['v2_up_count'] = data['data']['items'][i]['v2_up_count']
        except:
            result['v2_up_count'] = ''
        # details.append(result)
        details.append(encode_data(round(result['time']/1000,3), result['content'], result['id']))
    return details


# 输入关键信息
def count_danmu(num1, num2, page):
    danmu_total = []
    # num1 = input('第一个数字')
    # num2 = input('第二个数字')
    # page = int(input('输入总时长'))
    for i in range(page):
        danmu_total.extend(get_mgtv_danmu(num1, num2, i))
        time.sleep(0.1)

    return danmu_total


def main():
    # df = pd.DataFrame(count_danmu())
    # df.to_csv('mangguo_danmu.csv')

    # data = count_danmu("015611", "19684401", 35)
    # data = count_danmu("161302", "19684736", 33)
    # data = count_danmu("155638", "19685391", 39)
    data = count_danmu("082857", "19685311", 34)

    print(data)

    write_xml(data,"mg.xml")

if __name__ == '__main__':
    main()
