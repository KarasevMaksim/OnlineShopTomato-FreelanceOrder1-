from flask import render_template, uel_for, current_app
from app import db
from app.main import bp


@bp.route('/')
def index():
    render_template('index.html')