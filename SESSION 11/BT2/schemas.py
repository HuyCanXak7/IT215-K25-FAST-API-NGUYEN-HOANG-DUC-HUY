from pydantic import BaseModel, Field


class SmartHomePlanCreate(BaseModel):
    plan_code: str = Field(..., min_length=1)
    plan_name: str = Field(..., min_length=1)
    device_quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class SmartHomePlanResponse(BaseModel):
    id: int
    plan_code: str
    plan_name: str
    device_quantity: int
    price: float

    model_config = {
        "from_attributes": True
    } 