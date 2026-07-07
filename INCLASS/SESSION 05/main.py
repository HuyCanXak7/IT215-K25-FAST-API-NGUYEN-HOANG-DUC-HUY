from fastapi import FastAPI
from pydantic import BaseModel, Field 


class Userlogin(BaseModel):
    username:str
    password:str = Field(min_length=8)

@app.post("/auth/login")
def login(login_information: Userlogin):
    print(login_information)
    return 