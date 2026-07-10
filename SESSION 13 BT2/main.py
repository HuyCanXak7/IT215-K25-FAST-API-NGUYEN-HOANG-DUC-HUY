from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, get_db
from models import BoardingSlot
from schemas import (
    BoardingSlotCreate,
    BoardingSlotUpdate,
    BoardingSlotResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
def response(status_code, message, error, data, path):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
@app.post("/boarding-slots")
def create_slot(slot: BoardingSlotCreate, request: Request, db: Session = Depends(get_db)):
    try:
        existed = db.query(BoardingSlot).filter(
            BoardingSlot.slot_number == slot.slot_number
        ).first()

        if existed:
            return response(
                400,
                "Slot number already exists",
                "Bad Request",
                None,
                request.url.path
            )

        new_slot = BoardingSlot(**slot.model_dump())

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return response(
            201,
            "Thêm khoang lưu trú thành công",
            None,
            BoardingSlotResponse.model_validate(new_slot).model_dump(),
            request.url.path
        )

    except Exception:
        db.rollback()
        return response(500, "Internal Server Error", "Server Error", None, request.url.path)
    
@app.get("/boarding-slots")
def get_all_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(BoardingSlot).all()

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        [BoardingSlotResponse.model_validate(i).model_dump() for i in slots],
        request.url.path
    )

@app.get("/boarding-slots/{slot_id}")
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

    if not slot:
        return response(
            404,
            "Boarding slot not found",
            "Not Found",
            None,
            request.url.path
        )

    return response(
        200,
        "Lấy thông tin thành công",
        None,
        BoardingSlotResponse.model_validate(slot).model_dump(),
        request.url.path
    )
    
@app.put("/boarding-slots/{slot_id}")
def update_slot(slot_id: int, update: BoardingSlotUpdate, request: Request, db: Session = Depends(get_db)):
    try:
        slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

        if not slot:
            return response(
                404,
                "Boarding slot not found",
                "Not Found",
                None,
                request.url.path
            )

        data = update.model_dump(exclude_unset=True)

        if "slot_number" in data:
            existed = db.query(BoardingSlot).filter(
                BoardingSlot.slot_number == data["slot_number"],
                BoardingSlot.id != slot_id
            ).first()

            if existed:
                return response(
                    400,
                    "Slot number already exists",
                    "Bad Request",
                    None,
                    request.url.path
                )

        for key, value in data.items():
            setattr(slot, key, value)

        db.commit()
        db.refresh(slot)

        return response(
            200,
            "Cập nhật thành công",
            None,
            BoardingSlotResponse.model_validate(slot).model_dump(),
            request.url.path
        )

    except Exception:
        db.rollback()
        return response(500, "Internal Server Error", "Server Error", None, request.url.path)
    
@app.delete("/boarding-slots/{slot_id}")
def delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        slot = db.query(BoardingSlot).filter(BoardingSlot.id == slot_id).first()

        if not slot:
            return response(
                404,
                "Boarding slot not found",
                "Not Found",
                None,
                request.url.path
            )

        db.delete(slot)
        db.commit()

        return response(
            200,
            "Xóa khoang lưu trú thành công",
            None,
            None,
            request.url.path
        )

    except Exception:
        db.rollback()
        return response(500, "Internal Server Error", "Server Error", None, request.url.path)
    
