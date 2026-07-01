from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int


# Thêm học viên
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    if student.age <= 0:
        raise HTTPException(status_code=400, detail="Age must be greater than 0")

    for s in students:
        if s["code"] == student.code:
            raise HTTPException(status_code=400, detail="Student code already exists")

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Create student successfully",
        "data": new_student
    }


# Lấy danh sách + tìm kiếm + lọc
@app.get("/students")
def get_students(
    keyword: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None
):
    result = students

    if keyword:
        result = [
            s for s in result
            if keyword.lower() in s["name"].lower()
            or keyword.lower() in s["code"].lower()
            or keyword.lower() in s["email"].lower()
        ]

    if min_age is not None:
        result = [s for s in result if s["age"] >= min_age]

    if max_age is not None:
        result = [s for s in result if s["age"] <= max_age]

    return {
        "message": "Get students successfully",
        "data": result
    }


# Lấy chi tiết học viên
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return {
                "message": "Get student successfully",
                "data": student
            }

    raise HTTPException(status_code=404, detail="Student not found")


# Cập nhật học viên
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student.name.strip() == "":
        raise HTTPException(status_code=400, detail="Name cannot be empty")

    if student.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    if student.age <= 0:
        raise HTTPException(status_code=400, detail="Age must be greater than 0")

    for index, s in enumerate(students):
        if s["id"] == student_id:

            for item in students:
                if item["code"] == student.code and item["id"] != student_id:
                    raise HTTPException(status_code=400, detail="Student code already exists")

            students[index] = {
                "id": student_id,
                "code": student.code,
                "name": student.name,
                "email": student.email,
                "age": student.age
            }

            return {
                "message": "Update student successfully",
                "data": students[index]
            }

    raise HTTPException(status_code=404, detail="Student not found")


# Xóa học viên
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            deleted_student = students.pop(index)
            return {
                "message": "Delete student successfully",
                "data": deleted_student
            }

    raise HTTPException(status_code=404, detail="Student not found")