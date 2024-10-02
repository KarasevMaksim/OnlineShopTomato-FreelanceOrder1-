import json

from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
from app.models import Products, Sections, SubSections
from app.basket import bp


@bp.route('/')
def index():
    data_basket = request.cookies.get('data_basket')
    if data_basket:
        data_basket = json.loads(data_basket)
        basket_items = list(data_basket.items())
        products_and_count = [
            (Products.query.get(int(i[0])), i[1]) for i in basket_items
        ]
    
    return render_template(
        'basket/basket.html',
        products_and_count=products_and_count
    )
    