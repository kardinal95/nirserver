from twisted.internet import reactor
from py.net.NIRProtocol import NIRProtocol as prot
from py.net.NIRFactory import NIRFactory as fact
import shutil
import os
from logger import logger, make_logger


def main():
    port = 1079
    clear_old()

    factory = fact()
    factory.protocol = prot
    reactor.listenTCP(port, factory)
    logger.info('Starting listening on port {}...'.format(port))
    reactor.run()


def clear_old():
    logger.info('Clearing leftover files...')
    leftovers = os.listdir('temp')
    for item in leftovers:
        logger.debug('Removing {}'.format(item))
        shutil.rmtree(os.path.join('temp', item), True)
    logger.info('Successful!')

if __name__ == '__main__':
    main()