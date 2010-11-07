from irclib import irclib

class IRCBot:
    def __init__(self, server, port, nick, channels):
        self.irc = irclib.IRC()
        self.connection = self.irc.server()
        self.connection.connect(server, port, nick)

        self.irc.add_global_handler("all_events", self._dispatcher, -10)

        self.server = server
        self.port = port
        self.nick = nick
        self.channels = channels

    def _dispatcher(self, c, e):
        """[Internal]"""
        m = "on_" + e.eventtype()
        if hasattr(self, m):
            getattr(self, m)(c, e)

    def start(self):
        self.irc.start()
    def stop(self):
        self.irc.stop()

    def on_nicknameinuse(self, c, e):
        """nickname in use"""
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        """welcome message received"""
        for chan in [x.strip() for x in self.channels.split(",")]:
            c.join(chan)
        print "%s connected to %s successfully" % (self.nick, self.server)
