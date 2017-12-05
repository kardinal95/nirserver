from twisted.internet.protocol import Factory
from logger import logger


class NIRFactory(Factory):
    passhashes = [b'12345']

    def passhash_valid(self, passhash):
        logger.debug('Probing passhash: {}'.format(passhash))
        return passhash in self.passhashes
