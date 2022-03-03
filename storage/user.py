from distutils.command.build_scripts import first_line_re
from inspect import trace
from sqlalchemy import Column, Integer, String, DateTime
from base import Base
from datetime import datetime

class User(Base):
    """ User """

    __tablename__ = "User"
    
    personal_health_number = Column(String(12), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    postal_code = Column(String(7), nullable=False)
    street = Column(String(30), nullable=False)
    city = Column(String(30), nullable=False)
    province = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String(500), nullable=False)
    trace_id = Column(String(50), nullable = False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, personal_health_number, first_name, last_name, postal_code, street, city, province, country, age, password, trace_id):
        """ Initializes a blood pressure reading """
        self.personal_health_number = personal_health_number
        self.first_name = first_name
        self.last_name = last_name
        self.postal_code = postal_code
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.age = age
        self.password = password
        self.trace_id = trace_id
        self.date_created = datetime.now()


    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['personal_health_number'] = self.personal_health_number
        dict['first_name'] = self.first_name
        dict['last_name'] = self.last_name
        dict['postal_code'] = self.postal_code
        dict['street'] = self.street
        dict['city'] = self.city
        dict['province'] = self.province
        dict['country'] = self.country
        dict['age'] = self.age
        dict['password'] = self.password
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created
        return dict
