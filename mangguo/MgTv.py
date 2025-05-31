import json
import re
import time
import requests
from common.output import encode_data, write_xml
from common.utils import request_url_json


class MgTv:
    MANG_GUO_URL = "https://www.mgtv.com/"
    preg_id_text = r'/b/(\d+)/(\d+)'

    def search(self, keyword):
        url = "https://mobileso.bz.mgtv.com/msite/search/v2?q=我有一个朋友&pc=30&pn=1&sort=-99&ty=0&du=0&pt=0&corr=1&abroad=0&_support=10000000000000000"

        content = requests.get(url).content

        data = json.loads(content)

        list = data["data"]["contents"]

        res = []
        for i in list:
            if i["type"] != "media":
                continue

            for j in i["data"]:
                pattern = re.compile(self.preg_id_text)
                match = pattern.search(j["url"])
                if match:
                    item = {
                        "id": match.group(1),
                        "url": j["url"],
                        "title": j["title"].replace("<B>", "").replace("</B>", ""),
                        "jumpKind": j["jumpKind"]
                    }

                    res.append(item)

        print(len(res))

        return res

    def get_media_info(self, id, month=""):

        url = "https://pcweb.api.mgtv.com/variety/showlist?allowedRC=1&collection_id={}&month={}&page=1&_support=10000000".format(
            id, month)

        data = request_url_json(url)

        list = data["data"]["list"]
        res = []
        for i in list:
            val = {
                "video_id": i["video_id"],
                "t2": i["t2"],
                "url": i["url"],
            }
            res.append(val)

        return res

    def get_danmu_url(self, vid, cid):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "referer": 'https://www.mgtv.com/',
        }
        url = "https://galaxy.bz.mgtv.com/getctlbarrage?version=8.1.39&abroad=0&uuid=&os=10.0&platform=0&deviceid=6a3a516d-dfd8-49bc-bec2-75563bae620d&mac=&vid={}&pid=&cid={}&ticket="
        url = url.format(vid, cid)
        content = requests.get(url, headers=headers).content

        req = json.loads(content)
        data = req["data"]

        cdn_list = str(data["cdn_list"]).split(",")

        return "https://" + cdn_list[0] + "/" + data["cdn_version"]

    def get_danmu_info(self, prefix_url, page):
        danmu_total = []
        if page < 0:
            page = 10000
        # page = int(input('输入总时长'))
        for i in range(page):
            try:
                url = prefix_url + "/" + str(i) + ".json"
                # print("正在爬取第" + str(i) + "页")
                res = requests.get(url)

                if res.status_code == 404:
                    print(f"搜刮完成，共搜刮 {i} 页")
                    break

                data = json.loads(res.content)
                details = []
                items = data.get("data", {}).get("items", [])
                if items is None:
                    continue
                for i in range(len(items)):  # 弹幕数据在json文件'data'的'items'中
                    dm_content = data['data']['items'][i]['content']  # 获取弹幕内容
                    dm_time = data['data']['items'][i]['time']  # 获取弹幕发布时间
                    dm_id = data['data']['items'][i]['id']  # 获取id

                    try:  # 尝试获取弹幕点赞数
                        v2_stars = data['data']['items'][i]['v2_up_count']
                    except:
                        v2_stars = ''
                    # details.append(result)
                    details.append(encode_data(round(dm_time / 1000, 3), dm_content, dm_id))

                danmu_total.extend(details)
                time.sleep(0.1)
            except Exception as e:
                print(f"捕获到异常: {e}")
                raise e
        return danmu_total

    def start_scraper(self, name, someone=""):
        media_list = self.search(name)
        media = None
        for i in media_list:
            if i["title"] == name:
                media = i
                break

        if None == media:
            print("未找到相关资源")
            return

        print(f"找到资源：{media}")
        cid = media["id"]
        play_list = self.get_media_info(cid)

        for play in play_list:
            vid = play["video_id"]
            name = play["t2"]
            base_url = self.get_danmu_url(vid, cid)

            name_number = re.search(r"(\d+)", name).group()
            if name_number != "":
                name_number = "{:02d}".format(int(name_number))

            if "" != someone and someone != name_number:
                continue

            print(f"{name} 搜刮开始.....")
            try:
                dm_data = self.get_danmu_info(base_url, -1)
                write_xml(dm_data, "S01E" + name_number + ".xml")
            except:
                print(f"{name} 搜刮失败")
            time.sleep(1)
            # return
