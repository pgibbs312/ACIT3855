from sqlalchemy import Column, Integer, String, DateTime
from base import Base
class Stats(Base):
    """ Processing Statistics """
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_scores = Column(Integer, nullable=False)
    top_score = Column(Integer, nullable=False)
    low_score = Column(Integer, nullable=False)
    longest_run = Column(String, nullable =False)
    shortest_run = Column(String, nullable=False)
    num_users = Column(Integer, nullable=False)
    last_updated = Column(String, nullable=False)

    def __init__(self, num_scores, top_score, low_score, longest_run, shortest_run, num_users, last_updated):
        self.num_scores = num_scores
        self.top_score = top_score
        self.low_score = low_score
        self.longest_run = longest_run
        self.shortest_run = shortest_run
        self.num_users = num_users
        self.last_updated = last_updated
    
    def to_dict(self):
        dict = {}
        dict['num_scores'] = self.num_scores
        dict['top_score'] = self.top_score
        dict['low_score'] = self.low_score
        dict['longest_run'] = self.longest_run
        dict['shortest_run'] = self.shortest_run
        dict['num_users'] = self.num_users
        dict['last_updated'] = self.last_updated #.strftime("%Y-%m-%dT%H:%M:%S")

        return dict