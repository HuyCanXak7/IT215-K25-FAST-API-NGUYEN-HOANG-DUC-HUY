from fastapi import FastAPI

app = FastAPI()

@app.get("/students")
def get_students():
    return {
        "message": "Lấy danh sách sinh viên thành công"
    }

@app.get("/students/detail")
def get_student_detail():
    return {
        "message": "Xem chi tiết sinh viên"
    }

@app.post("/students")
def create_student():
    return {
        "message": "Thêm sinh viên mới thành công"
    }

@app.put("/students/update")
def update_student():
    return {
        "message": "Cập nhật thông tin sinh viên thành công"
    }

@app.delete("/students/delete")
def delete_student():
    return {
        "message": "Xóa sinh viên thành công"
    }

@app.get("/students/statistics")
def get_student_statistics():
    return {
        "message": "Thống kê sinh viên"
    }

@app.get("/students/active")
def get_active_students():
    return {
        "message": "Danh sách sinh viên đang học"
    }

@app.get("/students/top")
def get_top_students():
    return {
        "message": "Danh sách sinh viên tiêu biểu"
    }