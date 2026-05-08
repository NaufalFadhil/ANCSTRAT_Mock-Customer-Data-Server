from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class CustomerResponse(BaseModel):
  customer_id: str
  first_name: str
  last_name: str
  email: str
  phone: Optional[str] = None
  address: Optional[str] = None
  date_of_birth: Optional[date] = None
  account_balance: Optional[Decimal] = None
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True
