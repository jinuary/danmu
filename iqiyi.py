import zlib
import requests


# 1.爬取xml文件
def download_xml(url):
    bulletold = requests.get(url).content  # 二进制内容
    return zipdecode(bulletold)


def zipdecode(bulletold):
    '对zip压缩的二进制内容解码成文本'
    decode = zlib.decompress(bytearray(bulletold), 15 + 32).decode('utf-8')
    return decode


for x in range(1, 12):
    # x是从1到12，12怎么来的，这一集总共57分钟，爱奇艺每5分钟会加载新的弹幕,57除以5向上取整
    url = 'https://cmts.iqiyi.com/bullet/62/00/5981449914376200_300_' + str(x) + '.z'
    xml = download_xml(url)
    # 把编码好的文件分别写入17个xml文件中（类似于txt文件），方便后边取数据
    with open('./aiqiyi/iqiyi' + str(x) + '.xml', 'a+', encoding='utf-8') as f:
        f.write(xml)

# 2.读取xml文件中的弹幕数据数据
from xml.dom.minidom import parse
import xml.dom.minidom


def xml_parse(file_name):
    DOMTree = xml.dom.minidom.parse(file_name)
    collection = DOMTree.documentElement
    # 在集合中获取所有entry数据
    entrys = collection.getElementsByTagName("entry")
    print(entrys)
    result = []
    for entry in entrys:
        content = entry.getElementsByTagName('content')[0]
        print(content.childNodes[0].data)
        i = content.childNodes[0].data
        result.append(i)
    return result


# with open("aiyiqi_danmu.txt", mode="w", encoding="utf-8") as f:
#     for x in range(1, 12):
#         l = xml_parse("./aiqiyi/iqiyi" + str(x) + ".xml")
#         for line in l:
#             f.write(line)
#             f.write("\n")