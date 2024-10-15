import requests


class Mgtv:

    def search(self,keyword):
        url = "https://mobileso.bz.mgtv.com/msite/search/v2?q=我有一个朋友&pc=30&pn=1&sort=-99&ty=0&du=0&pt=0&corr=1&abroad=0&_support=10000000000000000"

        req = requests.get(url).content
