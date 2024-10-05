import json

from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
from app.models import Products, Sections, SubSections
from app.basket import bp


@bp.route('/')
def index():
    products_and_count = list()
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
    
    
@bp.route('/delete-product', methods=['POST'])
def delete_product():
    response = make_response(redirect(url_for('basket.index')))
    data_id = request.form.get('get_id')
    data_basket_json = request.cookies.get('data_basket')
    if data_basket_json:
        data_basket = json.loads(data_basket_json)
        if len(data_basket.keys()) == 1:
            response.delete_cookie('data_basket')
        else:
            del data_basket[data_id]
            data_basket_json = json.dumps(data_basket)
            response.set_cookie(
                'data_basket',
                data_basket_json,
                max_age=60*60*24
            )
        return response
    return redirect(url_for('basket.index'))


@bp.route('/update-product-in-basket', methods=['POST'])
def update_product_in_basket():
    product_id = request.form.get('get_id')
    cost = request.form.get('cost')
    response = make_response(redirect(url_for('basket.index')))
    if product_id and cost:
        data_basket_json = request.cookies.get('data_basket')
        if data_basket_json:
            data_basket = json.loads(data_basket_json)
            
            if data_basket.get(product_id) == cost:
                return redirect(url_for('basket.index'))

            data_basket[product_id] = cost
            data_basket_json = json.dumps(data_basket)
            response.set_cookie(
                'data_basket',
                data_basket_json,
                max_age=60*60*24
            )
            flash('Товары успешно обновлены!')
            return response
                
    return abort(404)


@bp.route('by-basket', methods=['POST'])
def by_basket():
    response = make_response()
    return render_template('basket/by.html')
