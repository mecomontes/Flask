from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BAse = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, unique=True, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    contact_info = relationship('ContactInfo', uselist=False, back_populates='students')

