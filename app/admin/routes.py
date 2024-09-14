from flask import render_template
# from app.admin.forms import *
from app.admin import bp
from app import db, login


@bp.route('/')
def admin():
    return render_template('admin/admin.html')


@bp.route('/login')
def login():
    return render_template('admin/login.html')
