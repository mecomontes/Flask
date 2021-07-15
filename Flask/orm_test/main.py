from models.contact_info import ContactInfo
from models.student import Base, Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USERS = [{"id": 1, "first_name": "Tang", "last_name": "Sophie"},
         {"id": 2, "first_name": "Larry", "last_name": "Hudson"},
         {"id": 3, "first_name": "Peter", "last_name": "Parker"},
         {"id": 4, "first_name": "Mary", "last_name": "Jane"},
         {"id": 5, "first_name": "Tony", "last_name": "Stark"},
         {"id": 6, "first_name": "Steve", "last_name": "Rogers"},]

CONTACT_INFO = [{"id": 1, "student_id": 6, "city": "New York", "phone": "+3549812"},
                {"id": 2, "student_id": 4, "city": "San Francisco", "phone": "+6745821"},
                {"id": 3, "student_id": 2, "city": "Chicago", "phone": "+98732415"},]

DB_USER = 'user'
DB_PASSWORD = 'password'
DB = 'relationships'

engine = create_engine(f'mysql+mysqldb://{}:{}@localhost:3306/{}', DB_USER,
                       DB_PASSWORD, DB), pool_pre_ping=True)

Base.meatadata.drop_all(engine)  # Erase previous tables
Base.meatadata.create_all(engine)  # Create previous tables

# Create the data into the DB
# python3 -m orm_test.main

Session = sessionmaker(bind=engine)
session = Session()

for student in STUDENTS:
    new_user = Student(**student)
    session.add(new_user)

for contact in CONTACT_INFO:
    new_contat =ContactInfo(**contact)
    session.add(new_contact)

session.commit()

students = session.query(Student).all()  # SELECT * FROM students
students_contact = session.query(Student, ContactInfo).join(ContactInfo)

for student, contact in students_contact:
    print(student.first_name, student.last_name, contact.city, contact.phone)


students = session.query(Student).All()

for student in students:
    if student.contact_info:
        print(student.first_name, student.last_name,
              student.contact.city, student.contact.phone)

contact_info = session.query(Student).All()

for contact in contact_info:
    print(contact.student.first_name, contact.student.last_name,
          contact.city, contact.phone)


