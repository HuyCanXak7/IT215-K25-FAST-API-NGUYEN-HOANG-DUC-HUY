from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import ParkingSlot
from schemas import ParkingSlotCreate


def create_slot(db: Session, slot: ParkingSlotCreate):
    exist = db.query(ParkingSlot).filter(
        ParkingSlot.slot_code == slot.slot_code
    ).first()

    if exist:
        raise HTTPException(
            status_code=400,
            detail="Slot code already exists"
        )

    new_slot = ParkingSlot(
        slot_code=slot.slot_code,
        zone_name=slot.zone_name,
        max_weight=slot.max_weight
    )

    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


def get_slots(db: Session):
    return db.query(ParkingSlot).all()


def get_slot(db: Session, slot_id: int):
    slot = db.query(ParkingSlot).filter(
        ParkingSlot.id == slot_id
    ).first()

    if not slot:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return slot