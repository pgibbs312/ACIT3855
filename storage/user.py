from markupsafe import string
from sqlalchemy import Column, Integer, String, DateTime, null
from base import Base
import datetime

class User(Base):
    """ Game Users """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    trans_id = Column(String(250), nullable=False)
    user_id = Column(Integer, nullable=False)
    email = Column(String(250), nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(String(250), nullable=False)
    phoneNumber = Column(String(250), nullable=False)
    timeStamp = Column(DateTime, nullable=False)

    def __init__(self, trans_id, user_id, email, name, password, phoneNumber, timeStamp):
        """ Initializes users """
        self.trans_id = trans_id
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.phoneNumber = phoneNumber
        self.timeStamp = datetime.datetime.now()
    
    def to_dict(self):
        """ Dictionary for users """
        dict = {}
        dict['id'] = self.id
        dict['trans_id'] = self.trans_id
        dict['user_id'] = self.user_id
        dict['email'] = self.email
        dict['name'] = self.name
        dict['password'] = self.password
        dict['phoneNumber'] = self.phoneNumber
        dict['timeStamp'] = self.timeStamp

        return dict