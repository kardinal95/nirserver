from twisted.internet import reactor
from py.net.NIRProtocol import NIRProtocol as prot
from py.net.NIRFactory import NIRFactory as fact


def main():
    factory = fact()
    factory.protocol = prot
    reactor.listenTCP(1079, factory)
    reactor.run()


if __name__ == '__main__':
    main()
