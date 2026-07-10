from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/warehouse_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_code = Column(String(50), unique=True)
    status = Column(String(100))


app = FastAPI()


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: int):
    db = SessionLocal()

    try:
        shipment = (
            db.query(ShipmentModel)
            .filter(ShipmentModel.id == shipment_id)
            .first()
        )

        if shipment is None:
            raise HTTPException(
                status_code=404,
                detail="Không tìm thấy mã vận đơn"
            )

        return {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "status": shipment.status
        }

    finally:
        db.close()