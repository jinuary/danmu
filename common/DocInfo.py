from common.VideoInfo import VideoInfo


class DocInfo(object):
    def __init__(self, cid, title, video_list: list[VideoInfo]):
        self.cid = cid
        self.title = title
        self.video_list = video_list

    def __repr__(self):
        return f"DocInfo:{self.cid},{self.title},{self.video_list}"
