class VideoInfo:
    def __init__(self, vid, title, url):
        self.vid = vid
        self.title = title
        self.url = url

    def __repr__(self):
        return f'{self.vid}: {self.title} - {self.url}'
