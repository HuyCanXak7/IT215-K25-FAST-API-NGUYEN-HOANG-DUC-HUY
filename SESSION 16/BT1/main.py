from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Bảng trung gian
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True)
)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    # Quan hệ 1-N
    students = relationship("Student", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    # Khóa ngoại Department
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="students")

    # Quan hệ 1-1
    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False
    )

    # Quan hệ N-N
    courses = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    bio = Column(String(255))

    # unique=True để đảm bảo 1-1
    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        unique=True
    )

    student = relationship(
        "Student",
        back_populates="profile"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    # Quan hệ N-N
    students = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )