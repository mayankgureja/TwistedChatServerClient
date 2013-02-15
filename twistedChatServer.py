"""
twistedChatServer.py
Mayank Gureja
02/14/2013
ECEC 433
"""

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor


class ChatServer(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        print "INFO: Receiving connection from", self.transport.getPeer().host
        self.sendLine("<Server> What's your name?")

    def connectionLost(self, reason):
        print "INFO: %s just left the chat" % self.name
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("<Server> Name taken, please choose another.")
            return
        print "INFO: %s just joined the chat" % name
        self.sendLine("<Server> Welcome, %s!" % (name))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        print message
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class ChatServerFactory(Factory):

    def __init__(self):
        self.users = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        return ChatServer(self.users)


print "INFO: I am ready to chat with a new client!"
reactor.listenTCP(22222, ChatServerFactory())
reactor.run()
