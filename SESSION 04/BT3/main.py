from fastapi import FastAPI, HTTPException

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]


@app.get("/products")
def get_products(keyword: str = None, max_price: float = None):
    # Kiểm tra max_price
    if max_price is not None and max_price < 0:
        raise HTTPException(
            status_code=400,
            detail="max_price không được âm"
        )

    result = products

    # Tìm theo tên (không phân biệt hoa thường)
    if keyword is not None:
        result = [
            product for product in result
            if keyword.lower() in product["name"].lower()
        ]

    # Lọc theo giá
    if max_price is not None:
        result = [
            product for product in result
            if product["price"] <= max_price
        ]

    return result