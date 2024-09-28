from flask import render_template
import sqlalchemy as sa
from app.models import Products, Sections, SubSections
from app.main import bp
from app.main.forms import (
    ShowProductsForm
)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShowProductsForm()
    title = 'Tomato'
    products = Products.query.all()[::-1]
    return render_template(
        'index.html',
        title=title,
        products=products,
        form=form
    )

