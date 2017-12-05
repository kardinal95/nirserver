from twisted.internet.protocol import connectionDone
from twisted.protocols import basic
from py.core.SessionHandler import SessionHandler
import time


class NIRProtocol(basic.LineReceiver):
    logged = False
    sessions = dict()
    commands = dict()

    def connectionMade(self):
        super(NIRProtocol, self).connectionMade()
        self.transport.write(b'Welcome to NIR server. Enter your passhash: ')
        self.commands['ans'] = self.add_session
        self.commands['sts'] = self.get_status
        self.commands['gsr'] = self.get_session_result

    def rawDataReceived(self, data):
        self.clearLineBuffer()

    def check_passhash(self, line):
        self.logged = self.factory.passhash_valid(line)
        if self.logged:
            self.transport.write(b'Successful login!\r\n')
            return
        self.transport.write(b'Incorrect passhash! Enter again: ')

    def lineReceived(self, line):
        # TODO rewrite with better parsing
        # TODO Codes for commands separately?
        if not self.logged:
            self.check_passhash(line)
        else:
            output = self.execute(line.decode())
            self.transport.write(output.encode())

    def connectionLost(self, reason=connectionDone):
        self.clean()
        super().connectionLost(reason)

    def execute(self, commandline):
        raw = commandline.split(' ')
        if raw[0] not in self.commands.keys():
            return '404 - Command not found'
        return self.commands[raw[0]](raw[1:])

    def add_session(self, args):
        stamp = str(int(time.time()))
        session = SessionHandler(args, stamp=stamp)
        self.sessions[stamp] = session
        # TODO Check session errors (state?)
        self.sessions[stamp].run()
        # TODO Run session
        return '000 ' + stamp

    def get_status(self, args):
        if len(args) != 1:
            return '403 - Incorrect arguments'
        if args[0] not in self.sessions.keys():
            return '301 - Not found session'
        return '000 ' + self.sessions[args[0]].get_status()

    def get_session_result(self, args):
        if len(args) != 1:
            return '403 - Incorrect arguments'
        if args[0] not in self.sessions.keys():
            return '301 - Not found session'
        pretty = ''
        result = self.sessions[args[0]].result
        for item in result.keys():
            pretty += str(item) + ':' + ','.join(result[item]) + '\r\n'
        return '000 ' + pretty

    def clean(self):
        for item in self.sessions.keys():
            self.sessions[item].destroy()