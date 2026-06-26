from fastapi import FastAPI
app = FastAPI()
students = ["An", "Bình", "Cuong"]
@app.get("/Students")
def get_students():
    return (students)
