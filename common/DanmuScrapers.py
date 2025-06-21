from abc import abstractmethod


class DanmuScrapers:
    @abstractmethod
    def get_danmu(self, vid):
        pass

    @abstractmethod
    def search(self, name, cid=None, vid=None):
        pass

    @abstractmethod
    def get_doc_info(self, cid, name, vid=None):
        pass

    @abstractmethod
    def get_video_list(self, cid, vid=None):
        pass
