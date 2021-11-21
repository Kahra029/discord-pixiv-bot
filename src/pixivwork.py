import json
from logging import exception
from pixivpy3 import *

class Pixivwork():
    def __init__(self, artworkId):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.pixivToken = config['pixiv_refresh_token']
            self.downloadPath = config['download_path']
        self.pixiv = AppPixivAPI()
        self.pixiv.auth(refresh_token = self.pixivToken)
        self.artworkId = artworkId

    def getArtwork(self):
        result = self.pixiv.illust_detail(self.artworkId)
        print(result)
        title = result.illust.title
        user = result.illust.user.name
        artwork = result.illust.image_urls.large
        idx = artwork.find('master1200.')
        exteniton = artwork[idx:]
        fileName = self.artworkId + exteniton
        self.pixiv.download(artwork, path = self.downloadPath, name = fileName)

        return title, user, fileName

    def getArtworks(self):
        result = self.pixiv.illust_detail(self.artworkId)
        title = result.illust.title
        user = result.illust.user.name
        artworks = result.illust.meta_pages
        i = 0
        for artwork in artworks: 
            imageUrl = artwork.image_urls.large
            idx = imageUrl.find('master1200.')
            exteniton = imageUrl[idx:]
            fileName = f'{self.artworkId}{exteniton}'
            fileName = f'{str(i)}_{fileName}'
            self.pixiv.download(imageUrl, path = self.downloadPath, name = fileName)
            i = i + 1

        return title, user, fileName, i