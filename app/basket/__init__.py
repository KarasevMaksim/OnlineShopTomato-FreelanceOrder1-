from flask import Blueprint

bp = Blueprint('basket', __name__, url_prefix='/basket')

from app.basket import routes, forms