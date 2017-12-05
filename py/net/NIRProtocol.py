from twisted.internet.protocol import connectionDone
from twisted.protocols import basic
from py.core.SessionHandler import SessionHandler
import time
from logger import logger


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
        logger.info('New connection established!')

    def rawDataReceived(self, data):
        self.clearLineBuffer()

    def check_passhash(self, line):
        self.logged = self.factory.passhash_valid(line)
        if self.logged:
            self.send_response('000', 'Successful login')
            logger.info('User logged in!')
            return
        self.send_response('000', 'Incorrect passhash! Enter again: ', False)
        logger.warn('Incorrect passhash provided!')

    def send_response(self, code, response, endline=True):
        formatted = b''
        if str(code) != '999':
            formatted = str(code).encode() + b' '
        formatted += response.encode()
        if endline:
            formatted += b'\r\n'
        self.transport.write(formatted)

    def lineReceived(self, line):
        if not self.logged:
            self.check_passhash(line)
        else:
            self.execute(line.decode())

    def connectionLost(self, reason=connectionDone):
        logger.info('Lost connection with user. Cleaning...')
        self.clean()
        logger.info('Cleaned up. Closing current protocol...')
        super().connectionLost(reason)

    def execute(self, commandline):
        logger.debug('CMD: {}'.format(commandline))
        raw = commandline.split(' ')
        if raw[0] not in self.commands.keys():
            self.send_response('404', 'Command not found')
            return
        self.commands[raw[0]](raw[1:])

    def add_session(self, args):
        logger.info('Adding new session...')
        stamp = str(int(time.time()))
        session = SessionHandler(args, stamp=stamp)
        self.sessions[stamp] = session
        logger.info('Success!')
        logger.debug('Session stamp: {}'.format(stamp))
        # TODO Check session errors (state?)
        self.sessions[stamp].run()
        # TODO Run session
        self.send_response('000', stamp)

    def get_status(self, args):
        if len(args) != 1:
            self.send_response('403', 'Incorrect arguments')
            return
        if args[0] not in self.sessions.keys():
            self.send_response('301', 'Not found session')
            return
        self.send_response('000', self.sessions[args[0]].get_status())

    def get_session_result(self, args):
        if len(args) != 1:
            self.send_response('403', 'Incorrect arguments')
            return
        if args[0] not in self.sessions.keys():
            self.send_response('301', 'Not found session')
            return
        self.send_response('000', 'Results got')
        result = self.sessions[args[0]].result
        for item in result.keys():
            self.send_response('999', str(item) + ':' + ','.join(result[item]))

    def clean(self):
        for item in self.sessions.keys():
            logger.debug('Removing session {}...'.format(item))
            self.sessions[item].destroy()