from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models.customer import Customer
from schemas.customer import CustomerResponse
from services.ingestion import fetch_all_from_flask, upsert_customers

# Auto-create tables saat startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Pipeline Service")

@app.post("/api/ingest")
def ingest_data(db: Session = Depends(get_db)):
  try:
    raw_data = fetch_all_from_flask()
    count = upsert_customers(db, raw_data)
    return {"status": "success", "records_processed": count}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/customers", response_model=list[CustomerResponse])
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    return customers

@app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer

