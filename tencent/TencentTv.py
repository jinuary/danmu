import time

import requests

from common.DanmuScrapers import DanmuScrapers
from common.DocInfo import DocInfo
from common.VideoInfo import VideoInfo
from common.output import encode_data
from common.utils import request_url, request_url_json, request_post_json


class TencentTv(DanmuScrapers):
    search_url = "https://pbaccess.video.qq.com/trpc.videosearch.mobile_search.HttpMobileRecall/MbSearchHttp"
    danmu_base_url = "https://dm.video.qq.com/barrage/base/{vid}"
    danmu_url = "https://dm.video.qq.com/barrage/segment/{vid}/"

    HEADER = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0",
        "origin": "https://m.v.qq.com",
        "referer": "https://m.v.qq.com/",
    }

    def __init__(self):
        super().__init__()

    # 搜索
    def search(self, name, vid=None, cid=None):

        data = []

        querystring = {"vplatform": "3"}

        payload = {
            "version": "24060601",
            "clientType": 1,
            "filterValue": "",
            "uuid": "27149E41-A050-4B81-A036-06CF9BCEF751",
            "retry": 0,
            "query": name,
            "pagenum": 0,
            "pagesize": 14,
            "queryFrom": 0,
            "searchDatakey": "",
            "transInfo": "",
            "isneedQc": True,
            "preQid": "",
            "adClientInfo": "",
            "extraInfo": {"isNewMarkLabel": "1"}
        }

        res = request_post_json(self.search_url, payload, headers=self.HEADER, querystring=querystring)

        normalList = res['data']['areaBoxList'][0]

        if normalList:
            itemList = normalList['itemList']

            for item in itemList:
                videoInfo = item['videoInfo']

                if videoInfo is None:
                    continue

                if videoInfo["year"] is None:
                    continue
                docId = item["doc"]["id"]
                title = videoInfo["title"]

                if cid is not None and cid != docId:
                    continue

                video_list = []
                episodeInfoList = videoInfo["episodeSites"][0]["episodeInfoList"]

                for episodeInfo in episodeInfoList:

                    if vid is not None and vid != episodeInfo["id"]:
                        continue

                    video_list.append(VideoInfo(episodeInfo["id"], episodeInfo["title"], episodeInfo["url"]))

                # print(DocInfo(docId, title, video_list))

                if video_list:
                    data.append(DocInfo(docId, title, video_list))

        return data

    def get_danmu(self, vid):
        # vid = "q4101tkrmk8"
        data = []
        base_url = self.danmu_base_url.format(vid=vid)

        res = request_url_json(base_url, headers=self.HEADER)

        start = res["segment_start"]
        size = res["segment_span"]

        segment_index = res["segment_index"]
        if segment_index:

            sorted_keys = sorted(segment_index.keys(), key=lambda k: int(k))

            for key in sorted_keys:
                print(segment_index.get(key))

                segment = segment_index.get(key)

                segment_url = self.danmu_url.format(vid=vid) + segment["segment_name"]

                segment_data = request_url_json(segment_url, headers=self.HEADER)

                barrage_list = segment_data["barrage_list"]

                for barrage in barrage_list:
                    # print(barrage)
                    data.append(encode_data(int(barrage["time_offset"]) / 1000, barrage["content"], barrage["id"]))

                # break
            # 分段处理
            # i = start
            # while i in segment_index and size > 0:
            #     segment = segment_index.get(i)
            #     segment_url = self.danmu_url.format(vid) + segment["segment_name"]
            #
            #     segment_data = request_url_json(segment_url, headers=self.HEADER)
            #
            #     print(segment_data["barrage_list"])
            #
            #     # 请求间隔
            #     time.sleep(1)
            #
            #     # 循环控制
            #     i += size

        return data
