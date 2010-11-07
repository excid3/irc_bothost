#!/usr/bin/env python

# Database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Bot

# Dbus imports
import dbus
import dbus.service
import dbus.mainloop.glib as glib
import gobject

# Import bots
from bots import GoogleSearchBot


DATABASE = '../website/database.db'

BOT_MAP = {
    0 : 'LogBot',
    1 : 'pastebot',
    2 : GoogleSearchBot,
}

running_bots = {}


class BotManagerService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('com.excid3.bothost', 
                                        bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/com/excid3/bothost')
 
    @dbus.service.method('com.excid3.bothost')
    def update(self):
        return "Hello,World!"
    
    @dbus.service.method('com.excid3.bothost')
    def shutdown(self):
        print "quitting"
        loop.quit()

    @dbus.service.method('com.excid3.bothost')
    def new_bot(self, type, id, args):
        print "launching new bot %i..." % id
        running_bots[id] = BOT_MAP[type](*args)
        running_bots[id].start()

    @dbus.service.method('com.excid3.bothost')
    def delete_bot(self, id):
        print "deleting %i" % id
        running_bots[id].stop()

        
if __name__ == "__main__":
    # Initialize gtk threading
    gobject.threads_init()
    glib.DBusGMainLoop(set_as_default=True)
    glib.threads_init()

    # Connect to the database
    engine = create_engine('sqlite:///'+DATABASE)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    # Create the bots
    print "starting bots"
    for bot in session.query(Bot).all():
        running_bots[bot.id] = BOT_MAP[bot.type](bot.server,
                                                 bot.port,
                                                 bot.nick,
                                                 bot.channels)
        running_bots[bot.id].start()

    # Setup the dbus service
    try:
        print "starting dbus service"
        service = BotManagerService()
        loop = gobject.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        pass

    # Clean up after interrupt
    print "starting cleanup"
    for id, thread in running_bots.items():
        thread.stop()
    print "shutting down"


