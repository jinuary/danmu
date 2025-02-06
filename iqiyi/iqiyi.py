import json
import math

import brotli
import requests

import danmu_pb2
import execjs
from output import encode_data, write_xml


def get_danmu_data(tvid, nums):
    # 编译JavaScript运行环境

    js = open("main.js", 'r', encoding='utf-8').read()
    context = execjs.compile(js)
    result = context.call("getDanmuList", tvid, nums)

    return result


def parser_data(content):
    data = []
    out = brotli.decompress(bytearray(content))
    danmu = danmu_pb2.Danmu()
    danmu.ParseFromString(out)
    for entry in danmu.entry:
        for bulletInfo in entry.bulletInfo:
            print(
                [
                    bulletInfo.id, bulletInfo.content, bulletInfo.a3
                    , bulletInfo.a4
                    , bulletInfo.a5
                    , bulletInfo.showTime
                    , bulletInfo.a7
                    , bulletInfo.a8
                    , bulletInfo.a9])
            # data.append([bulletInfo.showTime, 1, 25, 16777215, bulletInfo.id, 0, 0, 0, bulletInfo.content])
            data.append(encode_data(bulletInfo.showTime, bulletInfo.content, bulletInfo.id))

    # print(danmu_data)

    return data


def get_tvid_danmu(tvid, time, file_name):
    # 每集弹幕ID【tvId】,分钟数,文件名
    # 控制台: https://mesh.if.iqiyi.com/player/lw/video/danmu/info?id=2110197535504400
    # rr = ["5253083326678500", 46, "6"]
    # rr = ["3615862831507900", 47, "7"]

    rr = [tvid, time, file_name]
    result = get_danmu_data(rr[0], rr[1])
    danmu_list = []
    for url in result:
        print(url)
        try:
            br = requests.get(url).content

            re = parser_data(br)

            for item in re:
                danmu_list.append(item)
        except Exception as e:
            print(f"捕获到异常: {e}")
            break

    write_xml(danmu_list, rr[2] + ".xml")


def main():
    url = "https://mesh.if.iqiyi.com/portal/lw/search/homePageV3?key=漂白"
    iqiyiidid = "kjnf5fzfi0"
    # result = get_danmu_data("4303318963025000", 44)
    # result = get_danmu_data("7114108093346600", 47)
    content = requests.get(url).content

    data = json.loads(content)

    templates = data["data"]["templates"]

    for info in templates:
        template = info["template"]

        if template == 101:
            albumInfo = info['albumInfo']
            pageUrl = albumInfo["pageUrl"]

            if iqiyiidid in pageUrl:
                videos = albumInfo["videos"]

                for video in videos:
                    title = video["title"]
                    tvid = video["qipuId"]
                    duration = video["duration"]
                    time = math.ceil(duration / 1000 / 60)

                    get_tvid_danmu(tvid, time, title)

    # print(content)


if __name__ == '__main__':
    main()
