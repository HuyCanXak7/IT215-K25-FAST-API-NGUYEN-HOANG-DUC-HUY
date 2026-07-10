from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from schemas import ParkingSlotCreate, ParkingSlotResponse
from crud import create_slot, get_slots, get_slot
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()


def response(
    status_code,
    message,
    error,
    data,
    path
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.post("/parking-slots", status_code=201)
def add_slot(
    slot: ParkingSlotCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        new_slot = create_slot(db, slot)

        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            ParkingSlotResponse.model_validate(new_slot).model_dump(),
            str(request.url.path)
        )

    except HTTPException as e:
        return response(
            e.status_code,
            e.detail,
            "Error",
            None,
            str(request.url.path)
        )


@app.get("/parking-slots")
def all_slots(
    request: Request,
    db: Session = Depends(get_db)
):
    slots = get_slots(db)

    data = [
        ParkingSlotResponse.model_validate(i).model_dump()
        for i in slots
    ]

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        str(request.url.path)
    )


@app.get("/parking-slots/{slot_id}")
def detail_slot(
    slot_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        slot = get_slot(db, slot_id)

        return response(
            200,
            "Lấy thông tin thành công",
            None,
            ParkingSlotResponse.model_validate(slot).model_dump(),
            str(request.url.path)
        )

    except HTTPException as e:
        return response(
            e.status_code,
            e.detail,
            "Not Found",
            None,
            str(request.url.path)
        )