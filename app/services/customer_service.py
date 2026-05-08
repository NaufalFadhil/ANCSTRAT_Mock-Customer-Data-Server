from app.utils.json_loader import load_customers
from app.utils.pagination import paginate

class CustomerService:

  @staticmethod
  def get_customers(page, limit):
    customers = load_customers()

    return paginate(
      customers,
      page,
      limit
    )
  
  def get_customer_by_id(customer_id):
    customers = load_customers()

    customer = next(
      (
        customer
        for customer in customers
        if customer["customer_id"] == customer_id
      ),
      None
    )

    return customer
