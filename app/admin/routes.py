from flask import render_template, request, url_for, redirect, flash, abort
from app.admin.forms import AddProductForm, AddSectionsForm, LoginForm
from app.admin import bp
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from app import db, login
from app.models import Sections, Users, Products
from app.admin.funcs import save_product_img, resized_image


@bp.route('/', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return abort(403)
    
    sections = [(i.name, i.name.capitalize()) for i in Sections.query.all()]
    form = AddProductForm()
    show_products = Products.query.all()[::-1]
    
    form.select_section.choices.extend(sections)
    
    if form.validate_on_submit():
        sections_name = form.select_section.data.lower()
        try:
            db_sections = Sections().query.filter(
                Sections.name == sections_name
            ).first()
            
            product = Products()
            product.section_id = db_sections.id
            product.name = form.name.data
            product.price = form.price.data
            if form.about.data:
                product.about = form.about.data
            file_img = form.upload.data
            path_to_save, path_to_db = save_product_img(file_img.filename, sections_name)
            file_img = resized_image(file_img)
            file_img.save(path_to_save)
            product.img_link = path_to_db
            db.session.add(product)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
        return redirect(url_for('admin.admin'))
        
    return render_template(
        'admin/admin.html',
        show_products = show_products,
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
    show_sections = Sections.query.all()[::-1]

    if form.validate_on_submit():
        sections = Sections()
        try:
            sections.name = form.name.data.lower()
            db.session.add(sections)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
        flash('Категория успешно добавлена!')
        return redirect(url_for('admin.add_sections'))

    return render_template(
        'admin/add_sections.html',
        show_sections=show_sections,
        form=form,
    )


@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    if current_user.is_admin:
        confirm = request.form.get('confirm')
        what_del = request.form.get('type')
        if confirm:
            if what_del == 'product':
                product_id = request.form.get('get-id')
                product = Products().query.filter(
                    Products.id == product_id
                ).first()
                if product:
                    try:
                        db.session.delete(product)
                        db.session.commit()
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                        flash("Не удалось выполнить операцию!\nПроверьте корректность вводимых данных!")
                        return redirect(url_for('admin.admin'))
                    
            elif what_del == 'sections':
                section_id = request.form.get('get-id')
                section = Sections.query.filter(
                    Sections.id == section_id
                ).first()
                if section:
                    try:
                        db.session.delete(section)
                        db.session.commit()
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                        flash('Не удалось выполнить операцию\nПроверьте корректность вводимых данных!')
                        return redirect(url_for('admin.add_sections'))        
            
            flash("Удаление выполнено успешно!")
            if what_del == 'sections':
                return redirect(url_for('admin.add_sections'))
            return redirect(url_for('admin.admin'))
        
        flash('Перед удалением отметьте подтверждение!')
        if what_del == 'sections':
            return redirect(url_for('admin.add_sections'))
        return redirect(url_for('admin.admin'))   
             
    return abort(403)


@bp.route('/update-product-status', methods=['POST'])
@login_required
def update_product_status():
    if current_user.is_admin:
        confirm = request.form.get('confirm')
        product_id = request.form.get('get-id')
        if confirm:
            product = Products().query.filter(
                Products.id == product_id
            ).first()
            if product:
                is_active = product.is_active
                try:
                    product.is_active = not is_active
                    db.session.add(product)
                    db.session.commit()
                except Exception as err:
                    db.session.rollback()
                    print(err)
                    flash("Не удалось выполнить операцию!\nПроверьте корректность вводимых данных!")
                    return redirect(url_for('admin.admin'))
                
                flash('Статус наличия продукта изменен!')
                return redirect(url_for('admin.admin'))
            
            flash('Продкут не найден!')
            return redirect(url_for('admin.admin'))

        flash('Перед изменением отметьте подтверждение!')
        return redirect(url_for('admin.admin'))
    
    return abort(403)
    