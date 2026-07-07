from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]

orders_db = []

class OrderCreate(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate):

    # Kiểm tra sản phẩm tồn tại
    product = next(
        (p for p in products_db if p["id"] == data.product_id),
        None
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )

    # Kiểm tra số lượng hợp lệ
    if data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    # Kiểm tra tồn kho
    if data.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    # Trừ kho
    product["stock"] -= data.quantity

    # Tạo đơn hàng
    order = {
        "id": len(orders_db) + 1,
        "product_id": data.product_id,
        "quantity": data.quantity,
        "total": product["price"] * data.quantity
    }

    orders_db.append(order)

    return {
        "message": "Tạo đơn hàng thành công",
        "data": order
    }