from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        full_name=student.full_name,
        email=student.email,
        major=student.major,
        gpa=student.gpa
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(db: Session, student_id: int, data: StudentCreate):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.full_name = data.full_name
    student.email = data.email
    student.major = data.major
    student.gpa = data.gpa

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}