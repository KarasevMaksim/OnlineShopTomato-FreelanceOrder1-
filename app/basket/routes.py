import json

from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
from app.models import Products, Sections, HistorySales, HistoryProducts
from app import db
from app.basket import bp
from app.email import send_mail, msg_basket_for_admin, msg_basket_for_user
from app.basket.forms import PlaceAnOrder
from config import Config


@bp.route('/')
def index():
    form = PlaceAnOrder()
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
        products_and_count=products_and_count,
        form=form
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
    form = PlaceAnOrder()
    def query_products(p_id, count):
        product = Products.query.filter(Products.id == p_id).first()
        product_dict = {
           'name': product.name,
           'about': product.about,
           'price': product.price,
           'count': count,
           'total': int(count) * int(product.price),
           'section': product.section.name,
           'sub_section': product.sub_section.name,
           'link': f'{Config.DOMAIN}{product.id}',
           'img_link': Config.DOMAIN[:len(Config.DOMAIN) - 1] + url_for(
               'static', filename=product.img_link
               )
        }
        return product_dict
        
    response = make_response(render_template('basket/by.html'))
    
    
    data_basket_json = request.cookies.get('data_basket')
    if  data_basket_json:
        data_basket = json.loads(data_basket_json)
        if not form.validate_on_submit():
            basket_items = list(data_basket.items())
            products_and_count = [
            (Products.query.get(int(i[0])), i[1]) for i in basket_items
            ]
            
            return render_template(
                    'basket/basket.html',
                    form=form,
                    products_and_count=products_and_count
            )

        products = tuple(map(
            lambda items: query_products(items[0], items[1]),
            data_basket.items()
            )
        )
        name = form.name.data
        email = form.email.data
        phone = form.phone_number.data
        total_sum = sum(map(lambda x: x['total'], products))
        
        try:
            sales = HistorySales()
            for product in products:
                history = HistoryProducts()
                history.name_user = name
                if product['about']:
                    history.about_product = product['about']
                else:
                    history.about_product = 'Нет описания'
                history.email_user = email
                history.phone_user = str(phone)
                history.name_product = product['name']
                history.name_product = product['name']
                history.price = product['price']
                history.total_price = int(product['total'])
                history.count = int(product['count'])
                history.img_link = product['img_link']
                history.section = product['section']
                history.sub_section = product['sub_section']
                history.link_to_product = product['link']
                sales.h_prod.append(history)
            db.session.add(sales)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
        finally:
            order_id = HistorySales.query.order_by(
                HistorySales.id.desc()
            ).first()
            order_id = order_id.id
        
        admin_msg = msg_basket_for_admin(order_id, name, email, phone, total_sum, products)
        user_msg = msg_basket_for_user(order_id, name, total_sum, products)
        send_mail(
            'Заказ в магазине!',
            [Config.MAIL_USERNAME],
            html_body=admin_msg
        )
        send_mail(
            'Tomato Shop',
            [email],
            html_body=user_msg
        )
        response.delete_cookie('data_basket')
        return response
    
    flash('Ваша корзина пустая!')
    return redirect(url_for('basket.index'))

    
    
    
