from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=engine)
db_session = Session()

Base = declarative_base()


class DBConnection:
    def save_in_db(self):
        try:
            db_session.add(self)
            db_session.commit()
            return True
        except IntegrityError:
            db_session.rollback()
            return False


class TopicMessage(Base, DBConnection):
    __tablename__ = 'topic_messages'
    id = Column(Integer, primary_key=True)
    text = Column(Text(1024))

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'TopicMessage({})'.format(self.text)


class StopAlbum(Base, DBConnection):
    __tablename__ = 'stop_albums'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    link = Column(String(64))
    pre_order = Column(Integer)

    def __init__(self, name, link, pre_order):
        self.name = name
        self.link = link
        self.pre_order = pre_order

    def __repr__(self):
        return 'StopAlbum({}, {}, {})'.format(self.name, self.link, self.pre_order)


class PaymentInfo(Base, DBConnection):
    __tablename__ = 'payment_info'
    id = Column(Integer, primary_key=True)
    first_msg = Column(Text(256))
    recipient = Column(String(128))
    card_number = Column(String(24))
    card_type = Column(String(128))
    end_msg = Column(Text(256))

    def __init__(self, first_msg, recipient, card_number, card_type, end_msg):
        self.first_msg = first_msg
        self.recipient = recipient
        self.card_number = card_number
        self.card_type = card_type
        self.end_msg = end_msg

    def __repr__(self):
        return 'PaymentInfo({}, {}, {}, {}, {})'.format(self.first_msg, self.recipient, self.card_number, self.card_type, self.end_msg)


Base.metadata.create_all(engine)
