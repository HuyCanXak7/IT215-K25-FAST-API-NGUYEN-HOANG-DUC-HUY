from fastapi import FastAPI, HTTPException, status

app = FastAPI()

orders_db = {
    1: {
        "code": "SP001",
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "code": "SP002",
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}


@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):
    try:
        order = orders_db.get(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy đơn hàng"
            )

        return {
            "payment_status": order["payment_status"],
            "method": order["method"]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống"
        )