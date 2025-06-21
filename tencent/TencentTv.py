import json
import time

import requests

from common.DanmuScrapers import DanmuScrapers
from common.DocInfo import DocInfo
from common.VideoInfo import VideoInfo
from common.output import encode_data
from common.utils import request_url, request_url_json, request_post_json


class TencentTv(DanmuScrapers):
    search_url = "https://pbaccess.video.qq.com/trpc.videosearch.mobile_search.HttpMobileRecall/MbSearchHttp"
    video_url = "https://pbaccess.video.qq.com/trpc.universal_backend_service.page_server_rpc.PageServer/GetPageData"
    danmu_base_url = "https://dm.video.qq.com/barrage/base/{vid}"
    danmu_url = "https://dm.video.qq.com/barrage/segment/{vid}/"

    HEADER = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0",
        "origin": "https://m.v.qq.com",
        "referer": "https://m.v.qq.com/",
    }

    def __init__(self):
        super().__init__()

    """
        https://v.qq.com/x/cover/mzc00200iyue5he/k410187y6uq.html
        https://v.qq.com/x/cover/cid/vid.html
        cid: 节目id
        vid: 电视剧每集id
    """

    # 搜索
    def search(self, name, cid=None, vid=None):

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

        # areaBoxList 相关内容
        # normalList 作品
        areaBoxList = res['data']['areaBoxList'][0]

        if areaBoxList:
            itemList = areaBoxList['itemList']

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

                if len(videoInfo["episodeSites"]) == 0:
                    continue

                episodeInfoList = videoInfo["episodeSites"][0]["episodeInfoList"]

                for episodeInfo in episodeInfoList:

                    if vid is not None and vid != episodeInfo["id"]:
                        continue

                    video_list.append(VideoInfo(episodeInfo["id"], episodeInfo["title"], episodeInfo["url"]))

                # print(DocInfo(docId, title, video_list))

                if video_list:
                    data.append(DocInfo(docId, title, video_list))

        # normalList 作品
        normalList = res['data']['normalList']

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

                if len(videoInfo["episodeSites"]) == 0:
                    continue

                videoNum = videoInfo["subjectDoc"]["videoNum"]
                episodeInfoList = videoInfo["episodeSites"][0]["episodeInfoList"]

                for episodeInfo in episodeInfoList:

                    if vid is not None and vid != episodeInfo["id"]:
                        continue

                    video_list.append(VideoInfo(episodeInfo["id"], episodeInfo["title"], episodeInfo["url"]))

                # print(DocInfo(docId, title, video_list))

                if not video_list:
                    continue
                if len(video_list) != videoNum:
                    video_list = self.get_video_list(docId, video_list[0].vid)

                data.append(DocInfo(docId, title, video_list))

        return data

    def get_doc_info(self, cid, name, vid=None):

        video_list = self.get_video_list(cid, vid)

        return DocInfo(cid, name, video_list)

    def get_video_list(self, cid, vid=None, page_context=None):

        header = self.HEADER
        header["referer"] = "https://v.qq.com"
        header["origin"] = "https://v.qq.com"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": "pgv_pvid=2223960832; RK=2NMwGpjnFS; ptcz=1d802f5158927605eb89e53e602048367e1d157c6d8b20a86c457cdc2cff64fd; qq_domain_video_guid_verify=ed4606640fc6aa9d; _qimei_uuid42=18c13132d2b1007270c17018bb28fd6eab634381ef; video_platform=2; _qimei_h38=e06de48d70c17018bb28fd6e0200000e118c13; video_guid=ed4606640fc6aa9d; _qimei_q32=ce83b41203fb5ec65b9226be43a2376f; _qimei_q36=229f06dab0c5f56f3f72f187300016818a0b; pac_uid=0_nsM6akZK7kc9N; yyb_muid=195841C434A96DF60ADA54D235D36C04; QIMEI32=ce83b41203fb5ec65b9226be43a2376f; QIMEI36=229f06dab0c5f56f3f72f187300016818a0b; vdevice_qimei36=229f06dab0c5f56f3f72f187300016818a0b; _qimei_fingerprint=314c7ca5de8e2fb3c115e1c581608cee; video_omgid=ed4606640fc6aa9d; pgv_info=ssid=s3452015536",
            "origin": "https://v.qq.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://v.qq.com/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        video_list = []

        querystring = {"video_appid": "3000010", "vversion_name": "8.2.96", "vversion_platform": "2"}

        payload = {
            "page_params": {
                "req_from": "web_vsite",
                "page_id": "vsite_episode_list",
                "page_type": "detail_operation",
                "id_type": "1",
                "page_size": "",
                "cid": cid,
                "vid": vid,
                "lid": "",
                "page_num": "",
                "page_context": "",
                "detail_page_type": "1"
            },
            "has_cache": 1
        }

        if page_context is not None:
            payload["page_params"]["page_context"] = page_context

        res = request_post_json(self.video_url, payload, headers=headers, querystring=querystring)
        module_data = res["data"]["module_list_datas"][0]["module_datas"][0]
        try:
            item_list = module_data["item_data_lists"]["item_datas"]

            for item in item_list:

                if item["item_id"] == '':
                    continue

                item_params = item["item_params"]
                item_is_trailer = item_params["is_trailer"]
                # 预告片
                if item_is_trailer == '1':
                    continue

                item_vid = item_params["vid"]
                item_cid = item_params["cid"]
                item_title = item_params["title"]
                item_url = "https://v.qq.com/x/cover/" + item_cid + "/" + item_vid + ".html"

                video_list.append(VideoInfo(item_vid, item_title, item_url))

        except Exception as e:
            print(f"捕获到异常: {e}")

        module_params = module_data["module_params"]
        tabs = json.loads(module_params["tabs"])

        tab_index = -1
        for tab in tabs:

            if tab['selected']:
                tab_index = 1
                continue

            if tab_index == -1:
                continue

            if not tab['selected']:
                next_list = self.get_video_list(cid, vid, tab['page_context'])
                video_list.extend(next_list)

        return video_list

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
