import json
from pixivpy3 import *

class PixivData():
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.__pixivToken = config['pixiv_refresh_token']
            self.__downloadPath = config['download_path']
        self.__pixiv = AppPixivAPI()

    @property
    def pixivToken(self):
        return self.__pixivToken

    @property
    def downloadPath(self):
        return self.__downloadPath

    @property
    def pixiv(self):
        return self.__pixiv

class PixivWork():
    def __init__(self, artworkId):
        self.__artworkId = artworkId

    @property
    def artworkId(self):
        return self.__artworkId

    @artworkId.setter
    def artworkId(self, val):
        self.__artworkId = val

    def getArtwork(self):
        p = PixivData()
        p.pixiv.auth(refresh_token = p.pixivToken)
        data = p.pixiv.illust_detail(self.artworkId)
        artwork = data.illust.image_urls.large
        exteniton = artwork[artwork.find('master1200.'):]
        fileName = f'{self.artworkId}{exteniton}'
        p.pixiv.download(artwork, path = p.downloadPath, name = fileName)
        result = {
            'title': data.illust.title,
            'user': data.illust.user.name,
            'fileName': fileName
        }
        return result

    def getArtworks(self):
        p = PixivData()
        p.pixiv.auth(refresh_token = p.pixivToken)
        data = p.pixiv.illust_detail(self.artworkId)
        artworks = data.illust.meta_pages
        i = 0
        for artwork in artworks: 
            imageUrl = artwork.image_urls.large
            exteniton = imageUrl[imageUrl.find('master1200.'):]
            artworkName = f'{self.artworkId}{exteniton}'
            fileName = f'{str(i)}_{artworkName}'
            p.pixiv.download(imageUrl, path = p.downloadPath, name = fileName)
            i = i + 1
        
        result = {
            'title': data.illust.title,
            'user': data.illust.user.name,
            'fileName': artworkName,
            'pageCount': data.illust.page_count,
        }
        return result