import requests
from MgTv import MgTv

mg = MgTv()

# play_list = mg.search("我有一个朋友")
# print(play_list)
# for i in play_list:
#     play_url = i["play_url"]


# play_list = mg.get_media_info("466047")
# print(play_list)

#
# base_url = mg.get_danmu_url("19684401","466047")
# print(base_url)


mg.start_scraper("我有一个朋友","")