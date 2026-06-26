from fastapi import FastAPI

app = FastAPI()
students = [
    {"id": 1, "Name": "An"},
    {"id": 2, "Name": "Binh"},
    {"id": 3, "Name": "Cuong"},
]
@app.get("/student")
def get_student():
    return students[0]