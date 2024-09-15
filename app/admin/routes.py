from flask import render_template, request, url_for, redirect
from app.admin.forms import AddProductForm, AddSectionsForm
from app.admin import bp
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from app import db, login
from app.models import Sections


@bp.route('/', methods=['GET', 'POST'])
# @login_required
def admin():
    sections = [(i.name, i.name.capitalize()) for i in Sections.query.all()]
    form = AddProductForm()
    
    form.select_section.choices.extend(sections)
    
    if form.validate_on_submit():
        print('\n\n', form.select_section.data, '\n\n')
        return redirect(url_for('admin.admin'))
        
    return render_template(
        'admin/admin.html',
        form=form,
    )


@bp.route('/login')
def login():
    return render_template('admin/login.html')


@bp.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@bp.route('/add-sections', methods=['GET', 'POST'])
# @login_required
def add_sections():
    form = AddSectionsForm()

    if form.validate_on_submit():
        print('\n\n', form.name.data, '\n\n')
        return redirect(url_for('admin.add_sections'))

    return render_template(
        'admin/add_sections.html',
        form=form,
    )
