from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class Course(BaseModel):
    code: str
    name: str
    duration: int
    fee: float


# Thêm khóa học
@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: Course):
    for c in courses:
        if c["code"] == course.code:
            raise HTTPException(
                status_code=400,
                detail="Course code already exists"
            )

    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)
    return {
        "message": "Create course successfully",
        "data": new_course
    }


# Lấy danh sách + tìm kiếm + lọc
@app.get("/courses")
def get_courses(
    keyword: Optional[str] = None,
    min_fee: Optional[float] = None,
    max_fee: Optional[float] = None
):
    result = courses

    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c["name"].lower()
            or keyword.lower() in c["code"].lower()
        ]

    if min_fee is not None:
        result = [c for c in result if c["fee"] >= min_fee]

    if max_fee is not None:
        result = [c for c in result if c["fee"] <= max_fee]

    return {
        "message": "Get courses successfully",
        "data": result
    }


# Lấy chi tiết khóa học
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Get course successfully",
                "data": course
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


# Cập nhật khóa học
@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    for index, c in enumerate(courses):
        if c["id"] == course_id:

            for item in courses:
                if item["code"] == course.code and item["id"] != course_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Course code already exists"
                    )

            courses[index] = {
                "id": course_id,
                "code": course.code,
                "name": course.name,
                "duration": course.duration,
                "fee": course.fee
            }

            return {
                "message": "Update course successfully",
                "data": courses[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


# Xóa khóa học
@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for index, course in enumerate(courses):
        if course["id"] == course_id:
            deleted_course = courses.pop(index)
            return {
                "message": "Delete course successfully",
                "data": deleted_course
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )