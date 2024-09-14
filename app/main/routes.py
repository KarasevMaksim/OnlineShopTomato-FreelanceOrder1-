from flask import render_template
import sqlalchemy as sa
from app.models import Users
from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html')
