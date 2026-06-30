from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# Danh sách học viên hiện có
students = [
    {
        "full_name": "Existing Student",
        "email": "existing@gmail.com",
        "age": 22,
        "course": "python",
        "phone": "0900000000"
    }
]

# Model dữ liệu
class Student(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int
    course: str
    phone: str

# API đăng ký học viên
@app.post("/students")
def create_student(student: Student):
    # Kiểm tra email đã tồn tại
    for s in students:
        if s["email"] == student.email:
            raise HTTPException(
                status_code=400,
                detail="Email đã tồn tại trong hệ thống"
            )

    # Thêm học viên
    students.append(student.model_dump())

    return {
        "message": "Đăng ký học viên thành công",
        "student": student
    }