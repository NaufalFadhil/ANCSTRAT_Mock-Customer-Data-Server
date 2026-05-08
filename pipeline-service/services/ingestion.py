import os
import requests
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session
from models.customer import Customer

FLASK_BASE_URL = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000/api/customers")

def fetch_all_from_flask() -> list[dict]:
  all_customers = []
  page = 1
  limit = 10

  while True:
    response = requests.get(
      FLASK_BASE_URL,
      params={"page": page, "limit": limit}
    )

    response.raise_for_status()
    data = response.json()

    customers = data.get("data", [])
    if not customers:
      break

    all_customers.extend(customers)

    if page >= data.get("total_pages", 1):
      break

    page += 1

  return all_customers

def parse_date(value) -> date | None:
  if not value:
    return None
  try:
    return datetime.strptime(value, "%Y-%m-%d").date()
  except (ValueError, TypeError):
    return None


def parse_datetime(value) -> datetime | None:
  if not value:
    return None
  try:
    return datetime.fromisoformat(value)
  except (ValueError, TypeError):
    return None

def upsert_customers(db: Session, customers_data: list[dict]) -> int:
  count = 0

  for item in customers_data:
    customer_id = item.get("customer_id")
    existing = db.query(Customer).filter(
      Customer.customer_id == customer_id
    ).first()

    if existing:
      existing.first_name      = item.get("first_name")
      existing.last_name       = item.get("last_name")
      existing.email           = item.get("email")
      existing.phone            = item.get("phone")
      existing.address         = item.get("address")
      existing.date_of_birth   = parse_date(item.get("date_of_birth"))
      existing.account_balance = Decimal(str(item["account_balance"])) if item.get("account_balance") is not None else None
      existing.created_at      = parse_datetime(item.get("created_at"))
    else:
      new_customer = Customer(
        customer_id     = customer_id,
        first_name      = item.get("first_name"),
        last_name       = item.get("last_name"),
        email           = item.get("email"),
        phone           = item.get("phone"),
        address         = item.get("address"),
        date_of_birth   = parse_date(item.get("date_of_birth")),
        account_balance = Decimal(str(item["account_balance"])) if item.get("account_balance") is not None else None,
        created_at      = parse_datetime(item.get("created_at")),
      )
      db.add(new_customer)
    count += 1
  db.commit()
  return count
