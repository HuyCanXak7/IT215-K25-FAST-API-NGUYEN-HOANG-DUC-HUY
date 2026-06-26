from fastapi import FastAPI
app = FastAPI()
students = ["An", "Bình", "Cuong"]
@app.get("/getStudents")
def get_students():
    return "Danh sach sinh vien: "+ str(students)
