from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class MenuItemCreate(BaseModel):
    dish_code: str
    dish_name: str = Field(..., min_length=1)
    calorie_count: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: Literal["AVAILABLE", "OUT_OF_STOCK"]


class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = None
    dish_name: Optional[str] = Field(None, min_length=1)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["AVAILABLE", "OUT_OF_STOCK"]] = None


class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    model_config = ConfigDict(from_attributes=True)