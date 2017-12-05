from twisted.internet.protocol import Factory
from py.core.SessionHandler import SessionHandler
import time


class NIRFactory(Factory):
    passhashes = [b'12345']

    def passhash_valid(self, passhash):
        return passhash in self.passhashes
