from flask import Blueprint, request, jsonify
from app.services.customer_service import CustomerService

health_router = Blueprint("health", __name__)

@health_router.get("/")
def health_check():
  return jsonify({
    "success": True,
    "message": "Service is healty"
  }), 200
