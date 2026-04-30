from sqlalchemy import Column, String, Float
from database import Base


# טבלת מורות
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String(9), primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)


# טבלת תלמידות
class Student(Base):
    __tablename__ = "students"

    id = Column(String(9), primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)


# מיקום אחרון של תלמידה
class StudentLocation(Base):
    __tablename__ = "student_locations"

    student_id = Column(String(9), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)


# מיקום אחרון של מורה
class TeacherLocation(Base):
    __tablename__ = "teacher_locations"

    teacher_id = Column(String(9), primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)