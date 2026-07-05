from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

carriers = [
    {
        "id": 1,
        "code": "GHN",
        "name": "Giao Hang Nhanh",
        "max_weight_capacity": 5000,
        "status": "ACTIVE",
    },
    {
        "id": 2,
        "code": "GHTK",
        "name": "Giao Hang Tiet Kiem",
        "max_weight_capacity": 3000,
        "status": "ACTIVE",
    },
    {
        "id": 3,
        "code": "VTP",
        "name": "Viettel Post",
        "max_weight_capacity": 10000,
        "status": "SUSPENDED",
    },
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING",
    }
]


class Carrier(BaseModel):
    code: str
    name: str = Field(..., min_length=3)
    max_weight_capacity: int = Field(..., gt=0)
    status: Literal["ACTIVE", "INACTIVE", "SUSPENDED"]


class Shipment(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(..., gt=0)
    dispatch_date: str
    shift: Literal["MORNING", "AFTERNOON", "NIGHT"]


def find_carrier(carrier_id):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier
    return None


@app.post("/carriers", status_code=status.HTTP_201_CREATED)
def create_carrier(carrier: Carrier):
    for c in carriers:
        if c["code"].lower() == carrier.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Carrier code already exists"
            )

    new_carrier = carrier.model_dump()
    new_carrier["id"] = max([c["id"] for c in carriers], default=0) + 1

    carriers.append(new_carrier)

    return {
        "message": "Carrier created successfully",
        "data": new_carrier
    }


@app.get("/carriers")
def get_carriers(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_weight: Optional[int] = None
):
    result = carriers

    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c["code"].lower()
            or keyword.lower() in c["name"].lower()
        ]

    if status:
        result = [
            c for c in result
            if c["status"] == status
        ]

    if min_weight:
        result = [
            c for c in result
            if c["max_weight_capacity"] >= min_weight
        ]

    return result


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):
    carrier = find_carrier(carrier_id)

    if not carrier:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    return carrier


@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, carrier: Carrier):
    old = find_carrier(carrier_id)

    if not old:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    for c in carriers:
        if (
            c["id"] != carrier_id
            and c["code"].lower() == carrier.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Carrier code already exists"
            )

    old.update(carrier.model_dump())

    return {
        "message": "Carrier updated successfully",
        "data": old
    }


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    carrier = find_carrier(carrier_id)

    if not carrier:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    carriers.remove(carrier)

    return {
        "message": "Carrier deleted successfully"
    }


@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: Shipment):
    carrier = find_carrier(shipment.carrier_id)

    if not carrier:
        raise HTTPException(
            status_code=404,
            detail="Carrier not found"
        )

    if carrier["status"] != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Carrier is not ACTIVE"
        )

    if shipment.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Shipment exceeds carrier capacity"
        )

    for s in shipments:
        if (
            s["carrier_id"] == shipment.carrier_id
            and s["dispatch_date"] == shipment.dispatch_date
            and s["shift"] == shipment.shift
        ):
            raise HTTPException(
                status_code=400,
                detail="Carrier already has shipment in this shift"
            )

    new_shipment = shipment.model_dump()
    new_shipment["id"] = max([s["id"] for s in shipments], default=0) + 1

    shipments.append(new_shipment)

    return {
        "message": "Shipment created successfully",
        "data": new_shipment
    }


@app.get("/shipments")
def get_shipments():
    return shipments