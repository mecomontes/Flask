from sqlalchemy import Column, Integer, String, ForeingKey
from sqlalchemy.orm import relationship
from .student import Base

class ContactInfo(Base):
    __tablename__ = 'contact_info'
    id = Column(Integer, unique=True, primary_key=True)
    city = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    student_id = Column(Integer, ForeingKey('students.id'))
    student = relationship('Student', back_populates='contact_info')

