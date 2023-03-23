from flask import Blueprint
from .auth import auth

api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(auth)