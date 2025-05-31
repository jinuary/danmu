from pathlib import Path

from common.output import write_xml
from tencent.TencentTv import TencentTv


def write(danmu_data, file_name, dir_name):
    folder = Path("output" + "/" + dir_name)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)

    write_xml(danmu_data, folder.as_posix() + "/" + file_name + ".xml")


def main():
    scrapers = TencentTv()

    doc_list = scrapers.search("仙逆", vid="q4101tkrmk8")

    print(doc_list)

    for item in doc_list:

        video_list = item.video_list

        for video in video_list:
            danmu_data = scrapers.get_danmu(video.vid)
            write(danmu_data, video.title, item.title)


if __name__ == '__main__':
    main()
