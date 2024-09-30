import json

from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
import sqlalchemy as sa
from app.models import Products, Sections, SubSections
from app.slug import bp


@bp.route('/<int:id>')
def index(id):
    product = Products.query.get(id)
    if product and product.is_active:
        return render_template(
            'slug/product_card.html',
            product=product
        )
    abort(404)


@bp.route('/add-to-basket', methods=['POST'])
def add_to_basket():
    response = make_response(redirect(url_for('slug.index', id=product_id)))
    product_id = request.form.get('get_id')
    cost = request.form.get('cost')
    if product_id and cost:
        data_basket_json = request.cookies.get('data_basket')
        if data_basket_json:
            data_basket = json.loads(data_basket_json)
            if product_id in data_basket and data_basket[product_id] != cost:
                data_basket[product_id] = cost
                
                data_basket_json = json.dumps(data_basket)
                response.set_cookie(
                    'data_basket',
                    data_basket_json,
                    max_age=60*60*24    
                )
                flash("Товар успешно добавлен в корзину!")
                return response
                
    flash("Товар успешно добавлен в корзину!")
    return redirect(url_for('slug.index', id=product_id))