import execjs
import requests
import brotli
import danmu_pb2

# 编译JavaScript运行环境

js = open("main.js", 'r', encoding='utf-8').read()

# context = execjs.compile('''
#   function sayHello(name) {
#     return "Hello, " + name + "!";
#   }
# ''')
#
#
# # 在Python中执行JavaScript函数
# result = context.call('sayHello', 'World')


context = execjs.compile(js)
result = context.call("getDanmuList","4303318963025000",44)



# print(result)  # 输出: Hello, World!


def getBr(content):
    out = brotli.decompress(bytearray(content))
    danmu = danmu_pb2.Danmu()
    danmu.ParseFromString(out)
    # for entry in danmu.entry:
    #     for bulletInfo in entry.bulletInfo:
    #         danmu_data.append(bulletInfo.showTime)
    print([
        {bulletInfo.content, bulletInfo.showTime}
        for entry in danmu.entry
        for bulletInfo in entry.bulletInfo
    ])

    # print(danmu_data)


for url in result:
    print(url)
    br = requests.get(url).content
    getBr(br)