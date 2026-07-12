from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    major: str
    gpa: float


class StudentResponse(StudentCreate):
    id: int

    model_config = {
        "from_attributes": True
    }