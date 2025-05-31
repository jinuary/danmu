from abc import abstractmethod


class DanmuScrapers:
    @abstractmethod
    def get_danmu(self, vid):
        pass

    @abstractmethod
    def search(self, name, vid=None, cid=None):
        pass
