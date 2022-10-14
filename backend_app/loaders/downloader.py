#import pytube


# class YoutubeDownloader:
#     SUFFIX = 'v='

#     def __init__(self):
#         pass


#     def download(self, url: str):
#         output = url.rsplit(self.suffix, 1)[1]
#         yt = pytube.YouTube(url)
#         yt.streams.get_lowest_resolution().download(output)
#         return output