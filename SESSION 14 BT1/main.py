from fastapi import FastAPI

from app.database import Base, engine
from app.routers.product import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Management API")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Product Management API"}