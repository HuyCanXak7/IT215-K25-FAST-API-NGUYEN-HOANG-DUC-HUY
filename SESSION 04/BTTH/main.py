from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Danh sách khóa học
courses = [
    {
        "id": 1,
        "name": "Python Basic",
        "category": "backend",
        "price": 3000000,
        "mode": "online"
    },
    {
        "id": 2,
        "name": "Java Web",
        "category": "backend",
        "price": 5000000,
        "mode": "offline"
    },
    {
        "id": 3,
        "name": "Web Frontend",
        "category": "frontend",
        "price": 4000000,
        "mode": "online"
    }
]

# API 1: Lấy danh sách khóa học
@app.get("/courses")
def get_courses():
    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": courses
    }

# API 2: Lọc khóa học theo Query Parameters
@app.get("/courses/search")
def search_courses(
    mode: Optional[str] = None,
    category: Optional[str] = None
):
    result = courses

    if mode:
        result = [course for course in result if course["mode"] == mode]

    if category:
        result = [course for course in result if course["category"] == category]

    return {
        "message": "Lấy danh sách khóa học thành công",
        "data": result
    }

# API 3: Lấy chi tiết khóa học theo ID
@app.get("/courses/{course_id}")
def get_course_detail(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return {
                "message": "Tìm thấy khóa học",
                "data": course
            }

    return {
        "message": "Không tìm thấy khóa học"
    }
}