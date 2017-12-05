from twisted.protocols import basic


class NIRProtocol(basic.LineReceiver):
    logged = False

    def connectionMade(self):
        super(NIRProtocol, self).connectionMade()
        self.transport.write(b'Welcome to NIR server. Enter your passhash: ')

    def rawDataReceived(self, data):
        self.clearLineBuffer()

    def check_passhash(self, line):
        self.logged = self.factory.passhash_valid(line)
        if self.logged:
            self.transport.write(b'Successful login!\r\n')
            return
        self.transport.write(b'Incorrect passhash! Enter again: ')

    def lineReceived(self, line):
        if not self.logged:
            self.check_passhash(line)
        else:
            output = self.factory.execute(line.decode())
            self.transport.write(output.encode() + b'\r\n')