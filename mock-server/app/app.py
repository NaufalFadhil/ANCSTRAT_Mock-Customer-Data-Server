from flask import Flask

from app.routes.customer_routes import customer_router
from app.routes.health_routes import health_router

def create_app():
  app = Flask(__name__)
  app.url_map.strict_slashes = False

  app.register_blueprint(
      customer_router,
      url_prefix="/api/customers"
  )

  app.register_blueprint(
    health_router,
    url_prefix="/api/health"
  )

  return app
