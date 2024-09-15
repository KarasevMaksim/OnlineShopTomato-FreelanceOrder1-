from flask import render_template, request, url_for, redirect, flash, abort
from app.admin.forms import AddProductForm, AddSectionsForm, LoginForm
from app.admin import bp
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from app import db, login
from app.models import Sections, Users


@bp.route('/', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return abort(403)
    
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


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = Users.query.filter(Users.name == form.name.data).first()
        if user and user.is_admin and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('admin.admin'))
        
        flash('Не верный логин или пароль!')
        print('\n\n')
        return redirect(url_for('admin.login'))
            
    
    return render_template(
        'admin/login.html',
        form=form
    )


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


@bp.route('/add-sections', methods=['GET', 'POST'])
@login_required
def add_sections():
    if not current_user.is_admin:
        return abort(403)
    
    form = AddSectionsForm()

    if form.validate_on_submit():
        print('\n\n', form.name.data, '\n\n')
        return redirect(url_for('admin.add_sections'))

    return render_template(
        'admin/add_sections.html',
        form=form,
    )
