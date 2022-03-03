from imghdr import tests
from unittest import result
from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
from datetime import datetime


class rapid_test(Base):
    """ Blood Pressure """

    __tablename__ = "rapid_test"

    personal_health_number = Column(String(12), primary_key=True, nullable=False)
    manName = Column(String(250), nullable=False)
    homePage = Column(String(250), nullable=False)
    result_date = Column(String(100), nullable=False)
    rapid_test_result = Column(String(10), nullable=False)
    num_tests_taken = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    trace_id = Column(String(50), nullable = False)

    def __init__(self, personal_health_number, manName, homePage, result_date, rapid_test_result, num_tests_taken, trace_id):
        """ Initializes a blood pressure reading """
        self.personal_health_number = personal_health_number
        self.manName = manName
        self.homePage = homePage
        self.result_date = result_date
        self.rapid_test_result = rapid_test_result
        self.num_tests_taken = num_tests_taken
        self.date = datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['personal_health_number'] = self.personal_health_number
        dict['manufacturer'] = {}
        dict['manufacturer']['manName'] = self.manName
        dict['manufacturer']['homePage'] = self.homePage
        dict['result_date'] = self.result_date
        dict['rapid_test_result'] = self.rapid_test_result
        dict['num_tests_taken'] = self.num_tests_taken
        dict['date'] = self.date
        dict['trace_id'] = self.trace_id

        return dict
