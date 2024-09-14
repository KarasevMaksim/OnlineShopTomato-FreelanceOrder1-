from flask import render_template
# from app.admin.forms import *
from app.admin import bp
from flask_login import login_required
from app import db, login


@bp.route('/')
@login_required
def admin():
    return render_template('admin/admin.html')


@bp.route('/login')
def login():
    return render_template('admin/login.html')
