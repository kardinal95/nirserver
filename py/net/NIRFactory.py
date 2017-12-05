from twisted.internet.protocol import Factory
from py.core.SessionHandler import SessionHandler
import time


class NIRFactory(Factory):
    passhashes = [b'12345']
    sessions = dict()
    commands = dict()

    def __init__(self) -> None:
        super().__init__()
        self.commands['ans'] = self.add_session
        self.commands['sts'] = self.get_status

    def passhash_valid(self, passhash):
        return passhash in self.passhashes

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
        return '000 ' + self.sessions[args[0]].status
