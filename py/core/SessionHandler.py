from threading import Thread, Lock
from py.lib.vkapi import VkApiHandler
import urllib.request as rq
import os


class SessionHandler:
    ids = list()
    stamp = ''
    vk = None
    status = 'Waiting'

    def __init__(self, idlist, stamp):
        self.stamp = stamp
        self.ids = idlist
        self.vk = VkApiHandler(1)

    def run(self):
        os.makedirs(os.path.join('temp', self.stamp))
        for user in self.ids:
            self.parse_user(user)

    def parse_user(self, user):
        path = os.path.join('temp', self.stamp, user)
        os.makedirs(path)
        image_list = self.vk.process_user(user)
        lock = Lock()
        T = Thread(target=self.download_pictures, args=(image_list, lock, path))
        T.run()
        #file = open(os.path.join(path, 'pictures.lst'), 'w')
        #file.write('\n'.join(self.vk.process_user(user)))
        #file.close()

    def download_pictures(self, image_list, lock, path):
        for item in image_list:
            self.download_image(item, path)

    def download_image(self, image, path):
        name = image.split('/')[-1]
        rq.urlretrieve(image, os.path.join(path, name))