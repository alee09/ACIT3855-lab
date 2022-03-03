from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from base import Base

class Stats(Base):
        """processing statistics"""

        __tablename__ = "stats"

        id = Column(Integer, primary_key=True)
        num_tests_results = Column(Integer, nullable=False)
        num_users = Column(Integer, nullable=False)
        num_positive_tests = Column(Integer, nullable=False)
        num_negative_tests = Column(Integer, nullable=False)
        highest_positive_occuring_age = Column(Integer, nullable=False)
        last_updated = Column(DateTime, nullable=False)

        def __init__(self, num_tests_results, num_users, num_positive_tests, num_negative_tests, highest_positive_occuring_age, last_updated):
            """initializes a processing statistics obj"""
            self.num_tests_results = num_tests_results
            self.num_users = num_users
            self.num_positive_tests = num_positive_tests
            self.num_negative_tests = num_negative_tests
            self.highest_positive_occuring_age = highest_positive_occuring_age
            self.last_updated = last_updated
        
        def to_dict(self):
            """Dictionary Representation of a statistics"""
            dict = {}
            dict['num_tests_results'] = self.num_tests_results
            dict['num_users'] = self.num_users
            dict['num_positive_tests'] = self.num_positive_tests
            dict['num_negative_tests'] = self.num_negative_tests
            dict['highest_positive_occuring_age'] = self.highest_positive_occuring_age
            dict['last_updated'] = self.last_updated

            return dict
