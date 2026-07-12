from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student import (
    get_students,
    get_student,
    create_student,
    update_student,
    delete_student
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return get_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return get_student(db, student_id)


@router.post("/", response_model=StudentResponse)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)


@router.put("/{student_id}", response_model=StudentResponse)
def edit_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    return update_student(db, student_id, student)


@router.delete("/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    return delete_student(db, student_id)