from twisted.internet import reactor
from py.net.NIRProtocol import NIRProtocol as prot
from py.net.NIRFactory import NIRFactory as fact
import shutil, os


def main():
    clear_old()

    factory = fact()
    factory.protocol = prot
    reactor.listenTCP(1079, factory)
    reactor.run()


def clear_old():
    leftovers = os.listdir('temp')
    for item in leftovers:
        shutil.rmtree(os.path.join('temp', item), True)

if __name__ == '__main__':
    main()
