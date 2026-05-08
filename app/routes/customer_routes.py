from flask import Blueprint, request, jsonify
from app.services.customer_service import CustomerService

customer_router = Blueprint("customers", __name__)

@customer_router.get("/")
def get_customers():
  page = int(
    request.args.get("page", 1)
  )

  limit = int(
    request.args.get("limit", 10)
  )

  result = CustomerService.get_customers(
    page, 
    limit
  )

  return jsonify(result), 200

@customer_router.get("/<string:customer_id>")
def get_customer(customer_id):
  customer = CustomerService.get_customer_by_id(
    customer_id
  )

  if not customer:
    return jsonify({
      "message": "Customer not found"
    }), 404
  
  return jsonify(customer), 200
