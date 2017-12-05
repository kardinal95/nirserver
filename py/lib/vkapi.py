import urllib.request
import json
from logger import logger


class VkApiHandler:
    token = ''
    get_albums_api = 'https://api.vk.com/method/photos.getAlbums?&v=5.68&access_token='
    get_photos_api = 'https://api.vk.com/method/photos.get?&v=5.68&access_token='

    def __init__(self, token):
        token = '87581ab487581ab487581ab4a48706c0808875887581ab4de85f3e97c250d4ae2ca132b'
        logger.debug('API Token: {}'.format(token))
        self.token = token

    def process_user(self, user_id, quality='photo_604'):
        logger.info('Trying to process user with id {}...'.format(user_id))
        album_ids = self.get_album_ids(user_id)
        logger.debug('Acquired albums: {0}.'.format(', ').join(album_ids))
        photo_urls = self.get_photo_urls(album_ids, user_id, quality)
        logger.debug('Acquired {} photo links.'.format(len(photo_urls)))
        return photo_urls

    def get_album_ids(self, user_id):
        album_ids = list({'wall', 'profile', 'saved'})
        albums_get_url = '{}{}&owner_id={}'.format(self.get_albums_api, self.token, user_id)
        url_handler = urllib.request.urlopen(albums_get_url)
        response = url_handler.read().decode('utf-8')
        parsed = json.loads(response)
        album_count = parsed['response']['count']
        for current in range(0, album_count):
            album_ids.append(str(parsed['response']['items'][current]['id']))
        return album_ids

    def get_photo_urls(self, album_list, user_id, quality):
        photo_urls = list()
        for elem in album_list:
            photos_get_url = '{}{}&owner_id={}&album_id={}'.format(self.get_photos_api, self.token, user_id, elem)
            url_handler = urllib.request.urlopen(photos_get_url)
            response = url_handler.read().decode('utf-8')
            parsed = json.loads(response)
            if 'response' in parsed:
                photos_count = parsed['response']['count']
                for i in range (photos_count, 0, -1):
                    photo_urls.append(parsed['response']['items'][i - 1][quality])
        return photo_urls
