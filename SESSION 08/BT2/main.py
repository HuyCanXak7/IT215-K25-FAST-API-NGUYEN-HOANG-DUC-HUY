from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

app = FastAPI()

assets = [
    {
        "id": 1,
        "serial_number": "SN-MAC-01",
        "model": "MacBook Pro M3",
        "stock_available": 5,
        "status": "READY",
    },
    {
        "id": 2,
        "serial_number": "SN-DELL-02",
        "model": "Dell UltraSharp 27",
        "stock_available": 10,
        "status": "READY",
    },
    {
        "id": 3,
        "serial_number": "SN-THINK-03",
        "model": "ThinkPad X1 Carbon",
        "stock_available": 0,
        "status": "REPAIRING",
    },
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12,
    }
]


class Asset(BaseModel):
    serial_number: str
    model: str = Field(..., min_length=2, max_length=255)
    stock_available: int = Field(..., ge=0)
    status: Literal["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


class Allocation(BaseModel):
    asset_id: int
    employee_email: EmailStr
    allocated_quantity: int = Field(..., gt=0)
    start_date: str
    duration_months: int = Field(..., ge=1, le=12)


def find_asset(asset_id):
    for asset in assets:
        if asset["id"] == asset_id:
            return asset
    return None


@app.post("/assets", status_code=status.HTTP_201_CREATED)
def create_asset(asset: Asset):
    for a in assets:
        if a["serial_number"].lower() == asset.serial_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = asset.model_dump()
    new_asset["id"] = max([a["id"] for a in assets], default=0) + 1

    assets.append(new_asset)

    return {
        "message": "Asset created successfully",
        "data": new_asset
    }


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_stock: Optional[int] = None
):
    result = assets

    if keyword:
        result = [
            a for a in result
            if keyword.lower() in a["serial_number"].lower()
            or keyword.lower() in a["model"].lower()
        ]

    if status:
        result = [
            a for a in result
            if a["status"] == status
        ]

    if min_stock is not None:
        result = [
            a for a in result
            if a["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    asset = find_asset(asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset: Asset):
    old = find_asset(asset_id)

    if not old:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    for a in assets:
        if (
            a["id"] != asset_id
            and a["serial_number"].lower() == asset.serial_number.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    old.update(asset.model_dump())

    return {
        "message": "Asset updated successfully",
        "data": old
    }


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    asset = find_asset(asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    assets.remove(asset)

    return {
        "message": "Asset deleted successfully"
    }


@app.post("/allocations", status_code=status.HTTP_201_CREATED)
def create_allocation(allocation: Allocation):
    asset = find_asset(allocation.asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not READY"
        )

    if allocation.allocated_quantity > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    new_allocation = allocation.model_dump()
    new_allocation["id"] = max([a["id"] for a in allocations], default=0) + 1

    allocations.append(new_allocation)

    asset["stock_available"] -= allocation.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    return {
        "message": "Allocation created successfully",
        "data": new_allocation
    }


@app.get("/allocations")
def get_allocations():
    return allocations