from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal

class BoardingSlotCreate(BaseModel):
    slot_number: str
    room_size: Literal["SMALL", "MEDIUM", "LARGE"]
    price_per_day: float = Field(..., gt=0)
    status: Literal["VACANT", "OCCUPIED"]


class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str] = None
    room_size: Optional[Literal["SMALL", "MEDIUM", "LARGE"]] = None
    price_per_day: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["VACANT", "OCCUPIED"]] = None


class BoardingSlotResponse(BaseModel):
    id: int
    slot_number: str
    room_size: str
    price_per_day: float
    status: str

    model_config = ConfigDict(from_attributes=True)