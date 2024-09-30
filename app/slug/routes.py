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
    