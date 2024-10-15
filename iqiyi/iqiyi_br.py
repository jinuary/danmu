import brotli
import requests

import danmu_pb2
import xml.etree.ElementTree as ET
import execjs


def write_xml(data, filename="export.xml"):
    # 创建根元素
    root = ET.Element("i")

    # 添加命名空间属性
    root.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
    root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

    # 添加子元素
    ET.SubElement(root, 'chatserver').text = 'chat.bilibili.com'
    ET.SubElement(root, 'chatid').text = '10000'
    ET.SubElement(root, 'mission').text = '0'
    ET.SubElement(root, 'maxlimit').text = '8000'
    ET.SubElement(root, 'source').text = 'e-r'
    ET.SubElement(root, 'ds').text = '931869000'
    ET.SubElement(root, 'de').text = '937654881'
    ET.SubElement(root, 'max_count').text = '8000'

    for item in data:
        # 添加带有参数的 <d> 元素
        d1 = ET.SubElement(root, 'd')
        d1.text = item.pop(-1)
        str_list = [str(value) for value in item]
        d1.set('p', ",".join(str_list))

    # 生成 XML 字符串
    tree = ET.ElementTree(root)
    output_xml = ET.tostring(root, encoding='utf-8', method='xml').decode()

    print(output_xml)
    # 将XML树写入xml文件
    tree.write(filename, encoding="utf-8", xml_declaration=True)


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
            data.append([bulletInfo.showTime, 1, 25, 16777215, bulletInfo.id, 0, 0, 0, bulletInfo.content])

    # print(danmu_data)

    return data


def main():
    # result = get_danmu_data("4303318963025000", 44)
    # result = get_danmu_data("7114108093346600", 47)
    # rr = ["5253083326678500", 46, "6"]
    # rr = ["3615862831507900", 47, "7"]
    rr = ["6592700292338400", 47, "8"]
    result = get_danmu_data(rr[0], rr[1])
    danmu_list = []
    for url in result:
        print(url)
        br = requests.get(url).content

        re = parser_data(br)

        for item in re:
            danmu_list.append(item)

    write_xml(danmu_list, rr[2] + ".xml")


if __name__ == '__main__':
    main()
#
#
# with open("../4303318963025000_60_1_e09440ab.br", "rb") as f:
#     out = brotli.decompress(bytearray(f.read()))
#     danmu = danmu_pb2.Danmu()
#     danmu.ParseFromString(out)
#     for entry in danmu.entry:
#         for bulletInfo in entry.bulletInfo:
#             print(
#                 [
#                     bulletInfo.id, bulletInfo.content, bulletInfo.a3
#                     , bulletInfo.a4
#                     , bulletInfo.a5
#                     , bulletInfo.showTime
#                     , bulletInfo.a7
#                     , bulletInfo.a8
#                     , bulletInfo.a9])
#             danmu_data.append([bulletInfo.showTime, 1, 25, 16777215, bulletInfo.id, 0, 0, 0, bulletInfo.content])
#     # print([
#     #     {
#     #         bulletInfo.content,bulletInfo.showTime
#     #         ,bulletInfo.a4
#     #         ,bulletInfo.a5
#     #         ,bulletInfo.a6
#     #         ,bulletInfo.a7
#     #         ,bulletInfo.a8
#     #         ,bulletInfo.a9
#     #      }
#     #     for entry in danmu.entry
#     #     for bulletInfo in entry.bulletInfo
#     # ],end="\r\n")
#
#     print(danmu_data)
#     write_xml(danmu_data)
