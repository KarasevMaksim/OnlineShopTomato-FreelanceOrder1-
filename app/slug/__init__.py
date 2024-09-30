from flask import Blueprint

bp = Blueprint('slug', __name__)

from app.slug import routes