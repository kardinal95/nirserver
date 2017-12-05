import shutil
from threading import Thread, Event
from queue import Queue
from py.lib.vkapi import VkApiHandler
import urllib.request as rq
import os


class SessionHandler:
    def __init__(self, idlist, stamp):
        self.ids = list()
        for user in idlist:
            if user not in self.ids:
                self.ids.append(user)
        self.stamp = stamp
        self.queue = Queue()
        self.progress = Event()
        self.stop = Event()
        self.vk = VkApiHandler(1)
        self.result = dict()
        self.worker = Thread(target=self.parse_users, args=(self.queue,), daemon=True)

    def run(self):
        os.makedirs(os.path.join('temp', self.stamp))
        for user in self.ids:
            self.queue.put(user)
        self.worker.start()

    def parse_users(self, queue):
        self.progress.set()
        while not queue.empty() and not self.stop.is_set():
            user = queue.get()
            self.parse_user(user)
            queue.task_done()
        self.progress.clear()

    def parse_user(self, user):
        path = os.path.join('temp', self.stamp, user)
        os.makedirs(path)
        try:
            image_list = self.vk.process_user(user)
        except:
            self.result[user] = ['Incorrect user id']
        else:
            self.download_pictures(user, image_list, path)

    def download_pictures(self, user, image_list, path):
        for item in image_list:
            download_image(user, item, path)
            if self.stop.is_set():
                return
        self.result[user] = image_list

    def get_status(self):
        if self.progress.is_set():
            return 'Working'
        return 'Success'

    def destroy(self):
        self.stop.set()
        self.worker.join()
        shutil.rmtree(os.path.join('temp', self.stamp), True)
        #leftovers = os.listdir(os.path.join('temp', self.stamp))
        #for item in leftovers:
        #    shutil.rmtree(os.path.join('temp', self.stamp, item), True)

def download_image(self, image, path):
    name = image.split('/')[-1]
    rq.urlretrieve(image, os.path.join(path, name))

