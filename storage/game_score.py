# from tkinter.tix import COLUMN, INTEGER
from sqlalchemy import Column, Integer, String, DateTime, false, null
from base import Base
import datetime

class GameScore(Base):
    """ Game Score """
    __tablename__ = "game_score"

    id = Column(Integer, primary_key=True)
    trans_id = Column(String(250), nullable=False)
    score_id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    runTime = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    userName = Column(String(250), nullable=False)

    def __init__(self, trans_id, score_id, date, runTime, score, userName):
        """ Initializes scores """
        self.trans_id = trans_id
        self.score_id = score_id
        self.date = datetime.datetime.now()
        self.runTime = runTime
        self.score = score
        self.userName = userName
    
    def to_dict(self):
        """ Dictionary for scores """
        dict = {}
        dict['id'] = self.id
        dict['trans_id'] = self.trans_id
        dict['score_id'] = self.score_id
        dict['date'] = self.date
        dict['runTime'] = self.runTime
        dict['score'] = self.score
        dict['userName'] = self.userName

        return dict
