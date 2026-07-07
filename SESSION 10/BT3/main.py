from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
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


class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)


Base.metadata.create_all(bind=engine)


class InventoryCreate(BaseModel):
    warehouse_code: str
    location: str


app = FastAPI()


@app.post("/inventories", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: InventoryCreate):
    db = SessionLocal()

    try:
        existing_inventory = (
            db.query(InventoryModel)
            .filter(
                InventoryModel.warehouse_code == inventory.warehouse_code
            )
            .first()
        )

        if existing_inventory:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
            )

        new_inventory = InventoryModel(
            warehouse_code=inventory.warehouse_code,
            location=inventory.location
        )

        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return {
            "message": "Tạo phiếu kho vận thành công",
            "data": {
                "id": new_inventory.id,
                "warehouse_code": new_inventory.warehouse_code,
                "location": new_inventory.location
            }
        }

    finally:
        db.close()