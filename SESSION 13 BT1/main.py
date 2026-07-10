from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from database import Base, engine, get_db
from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse

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


# ==========================
# POST
# ==========================

@app.post("/menu-items")
def create_menu_item(
        item: MenuItemCreate,
        request: Request,
        db: Session = Depends(get_db)
):
    try:

        existed = db.query(MenuItem).filter(
            MenuItem.dish_code == item.dish_code
        ).first()

        if existed:
            return response(
                400,
                "Dish code already exists",
                "Bad Request",
                None,
                str(request.url.path)
            )

        menu = MenuItem(**item.model_dump())

        db.add(menu)

        db.commit()

        db.refresh(menu)

        return response(
            201,
            "Thêm món ăn thành công",
            None,
            MenuItemResponse.model_validate(menu).model_dump(),
            str(request.url.path)
        )

    except Exception:
        db.rollback()
        return response(
            500,
            "Internal Server Error",
            "Server Error",
            None,
            str(request.url.path)
        )


# ==========================
# GET ALL
# ==========================

@app.get("/menu-items")
def get_all_menu_items(
        request: Request,
        db: Session = Depends(get_db)
):

    items = db.query(MenuItem).all()

    data = [
        MenuItemResponse.model_validate(i).model_dump()
        for i in items
    ]

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        str(request.url.path)
    )


# ==========================
# GET ONE
# ==========================

@app.get("/menu-items/{item_id}")
def get_one(
        item_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    item = db.query(MenuItem).filter(
        MenuItem.id == item_id
    ).first()

    if not item:
        return response(
            404,
            "Menu item not found",
            "Not Found",
            None,
            str(request.url.path)
        )

    return response(
        200,
        "Lấy thông tin thành công",
        None,
        MenuItemResponse.model_validate(item).model_dump(),
        str(request.url.path)
    )


# ==========================
# PUT
# ==========================

@app.put("/menu-items/{item_id}")
def update_menu_item(
        item_id: int,
        update: MenuItemUpdate,
        request: Request,
        db: Session = Depends(get_db)
):

    try:

        menu = db.query(MenuItem).filter(
            MenuItem.id == item_id
        ).first()

        if not menu:
            return response(
                404,
                "Menu item not found",
                "Not Found",
                None,
                str(request.url.path)
            )

        data = update.model_dump(exclude_unset=True)

        if "dish_code" in data:
            existed = db.query(MenuItem).filter(
                MenuItem.dish_code == data["dish_code"],
                MenuItem.id != item_id
            ).first()

            if existed:
                return response(
                    400,
                    "Dish code already exists",
                    "Bad Request",
                    None,
                    str(request.url.path)
                )

        for key, value in data.items():
            setattr(menu, key, value)

        db.commit()

        db.refresh(menu)

        return response(
            200,
            "Cập nhật món ăn thành công",
            None,
            MenuItemResponse.model_validate(menu).model_dump(),
            str(request.url.path)
        )

    except Exception:
        db.rollback()
        return response(
            500,
            "Internal Server Error",
            "Server Error",
            None,
            str(request.url.path)
        )


# ==========================
# DELETE
# ==========================

@app.delete("/menu-items/{item_id}")
def delete_menu_item(
        item_id: int,
        request: Request,
        db: Session = Depends(get_db)
):

    try:

        menu = db.query(MenuItem).filter(
            MenuItem.id == item_id
        ).first()

        if not menu:
            return response(
                404,
                "Menu item not found",
                "Not Found",
                None,
                str(request.url.path)
            )

        db.delete(menu)

        db.commit()

        return response(
            200,
            "Xóa món ăn thành công",
            None,
            None,
            str(request.url.path)
        )

    except Exception:
        db.rollback()
        return response(
            500,
            "Internal Server Error",
            "Server Error",
            None,
            str(request.url.path)
        )