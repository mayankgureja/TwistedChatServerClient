"""
twistedChatClient.py
Mayank Gureja
02/14/2013
ECEC 433
"""

from twisted.internet import reactor, protocol, stdio
from twisted.protocols.basic import LineReceiver


class Server(LineReceiver):

    def connectionMade(self):
        self.factory = ChatClientFactory()
        self.connector = reactor.connectTCP('localhost', 22222, self.factory)

    def dataReceived(self, line):
        self.handle_CHAT(line)

    def handle_CHAT(self, message):
        if message and message.rstrip() != "quit()":
            self.connector.transport.write(message.rstrip() + '\r\n')
        else:
            print "\n* Goodbye! *\n"
            self.connector.transport.loseConnection()


class ChatClient(LineReceiver):

    def connectionMade(self):
        print "INFO: Connected to server", self.transport.getPeer().host

    def lineReceived(self, line):
        print line


class ChatClientFactory(protocol.ClientFactory):
    protocol = ChatClient

    def clientConnectionFailed(self, connector, reason):
        print "INFO: Connection failed - Goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "INFO: Connection lost - Goodbye!"
        reactor.stop()


stdio.StandardIO(Server())
reactor.run()
