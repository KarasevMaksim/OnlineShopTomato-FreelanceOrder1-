import json

from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
from app.models import Products, Sections, SubSections
from app.basket import bp


@bp.route('/')
def index():
    return render_template('basket/basket.html')