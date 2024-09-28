from flask import render_template
import sqlalchemy as sa
from app.models import Users, Products
from app.main import bp


@bp.route('/')
def index():
    title = 'Tomato'
    products = Products.query.all()
    return render_template(
        'index.html',
        title=title,
        products=products
    )

