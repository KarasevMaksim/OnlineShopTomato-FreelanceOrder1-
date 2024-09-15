from flask import render_template, request, url_for, redirect
from app.admin.forms import AddProductForm
from app.admin import bp
from flask_login import login_required
from app import db, login
from app.models import Sections


@bp.route('/', methods=['GET', 'POST'])
# @login_required
def admin():
    sections = [(i.name, i.name.capitalize()) for i in Sections.query.all()]
    form = AddProductForm()
    
    if request.method == "POST":
        print('\n\n', form.select_section.data, '\n\n')
        return redirect(url_for('admin.admin'))
    if request.method == "GET":
        form.select_section.choices.extend(sections)
        
    return render_template('admin/admin.html', form=form)


@bp.route('/login')
def login():
    return render_template('admin/login.html')
