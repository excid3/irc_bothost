
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bot(Base):
    __tablename__ = 'common_bot'

    id = Column(Integer, primary_key=True)
    owner = Column('owner_id', Integer) #TODO: Change to be a foreign key
    name = Column(String(36))
    nick = Column(String(36))
    type = Column(Integer)
    server = Column(Text)
    port = Column(Integer)
    channels = Column(String(2000))
    server_password = Column(String(36))
    nickserv_password = Column(String(36))
    status = Column(Integer)

    def __init__(self, owner, name, type, server, port, channels):
        self.owner = owner
        self.name = name
        self.type = type
        self.server = server
        self.port = port
        self.channels = channels

    def __repr__(self):
        return "<Bot('%s','%s','%s','%s','%s', '%s', '%s')>" % (self.id,
            self.owner, self.name, self.type, self.server, self.port,
            self.channels)

class BotData(Base):
    __tablename__ = 'common_botdata'

    id = Column(Integer, primary_key=True)
    bot = Column('bot_id', ForeignKey(Bot.id))
    date = Column(Date)
    time = Column(Time)
    content = Column(String(2000))

    def __init__(self, bot, date, time, content):
        self.bot = bot
        self.date = date
        self.time = time
        self.content = content

    def __repr__(self):
        return "<Update('%s','%s','%s','%s', '%s')>" % (self.id, self.bot,
                                            self.date, self.time, self.content)

if __name__ == "__main__":
    engine = create_engine('sqlite:///bothost.db')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    allbots = session.query(Bot).all()
    for bot in allbots:
        print bot

    allupdates = session.query(Update).all()
    for update in allupdates:
        print update

    allbotdata = session.query(BotData).all()
    for botdata in allbotdata:
        print botdata
