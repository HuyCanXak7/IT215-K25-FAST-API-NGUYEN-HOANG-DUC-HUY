from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import uuid

app = FastAPI()


class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11)
    course: str
    note: Optional[str] = Field(default=None, max_length=200)

    # Kiểm tra số điện thoại chỉ chứa chữ số
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa chữ số")
        return value

    # Chuẩn hóa họ tên
    @field_validator("full_name")
    @classmethod
    def normalize_name(cls, value):
        return " ".join(word.capitalize() for word in value.strip().split())

    # Chuẩn hóa ghi chú
    @field_validator("note")
    @classmethod
    def normalize_note(cls, value):
        if value is not None:
            return value.strip().lower()
        return value


@app.post("/students/register")
def register_student(student: StudentRegister):
    student_id = str(uuid.uuid4())[:8].upper()

    return {
        "message": "Đăng ký học viên thành công",
        "student_id": student_id,
        "data": student.model_dump()
    }