import xml.etree.ElementTree as ET


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


def encode_data(time, content, id):
    #时间（s）
    #弹幕类型 1 2 3:普通弹幕 4:底部弹幕 5:顶部弹幕 6:逆向弹幕 7:高级弹幕 8:代码弹幕 9:BAS弹幕(pool必须为2)
    #文字大小
    #弹幕颜色，默认白色16777215
    #发送时间
    #
    #用户id，Hash？ [mgtv]
    #
    #内容
    return [time, 1, 25, 16777215, id, 0, 0, 0, content]
