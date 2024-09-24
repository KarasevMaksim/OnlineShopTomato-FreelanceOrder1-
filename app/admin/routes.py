import json
from flask import (
    render_template, request, url_for, redirect, flash, abort, jsonify,
    make_response
)
from app.admin.forms import (
    AddProductForm, AddSectionsForm, AddSubSectionsForm, LoginForm,
    ShowProductsForm
)
from app.admin import bp
from flask_login import (
    current_user, login_user, logout_user, login_required
)
from app import db, login
from app.models import Sections, SubSections, Users, Products
from app.admin.funcs import (
    save_product_img, resized_image, delete_paths_to_img, delete_product_img
)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return abort(403)
    
    sections_item = Sections.query.all()
    sections = [(i.name, i.name.capitalize()) for i in sections_item]
    if sections_item:
        sub_sections = [
            (i.name, i.name.capitalize()) for i in sections_item[0].sub_sections
        ]
    
    form = AddProductForm()
    form2 = ShowProductsForm()
    
    show_products = Products.query.all()[::-1]
    if sections_item:
        form.select_section.choices.extend(sections)
        form.select_sub_section.choices.extend(sub_sections)
        form2.select_section2.choices.extend(sections)
        form2.select_sub_section2.choices.extend(sub_sections)
    if request.method == 'POST':
        try:
            if form.select_section.data:
                form.select_section.choices.extend(
                    [(form.select_section.data,
                    form.select_section.data.capitalize())]
                )
                form.select_sub_section.choices.extend(
                    [(form.select_sub_section.data,
                  form.select_sub_section.data.capitalize())]
                )
        except Exception as err:
            print(err)
            return redirect(url_for('admin.admin'))
        
    if request.method == 'POST' and form2.select_section2.data:
        sec_for_products = SubSections.query.filter(
            SubSections.name == form2.select_sub_section2.data
        ).first()
        if sec_for_products:
            show_products = sec_for_products.products[::-1]
    
    elif form.validate_on_submit():
        sub_sections_name = form.select_sub_section.data.lower()
        try:
            db_sub_sections = SubSections().query.filter(
                SubSections.name == sub_sections_name
            ).first()
            
            product = Products()
            product.name = form.name.data
            product.price = form.price.data
            if form.about.data:
                product.about = form.about.data
            file_img = form.upload.data
            path_to_save, path_to_db = save_product_img(
                file_img.filename,
                str(db_sub_sections.id)
            )
            file_img = resized_image(file_img)
            file_img.save(path_to_save)
            product.img_link = path_to_db
            db_sub_sections.products.append(product)
            db_sub_sections.section.products.append(product)
            db.session.add(db_sub_sections)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
        return redirect(url_for('admin.admin'))
        
    return render_template(
        'admin/admin.html',
        show_products = show_products,
        form=form,
        form2=form2
    )
    
    
@bp.route('/get_sub_sections', methods=['POST'])
@login_required
def get_sub_sections():
    if not current_user.is_admin:
        return abort(403)
    
    data = request.get_json()
    section_name = data.get('section')

    if section_name is None:
        return jsonify({'error': 'No section provided'}), 400

    sub_sections = Sections.query.filter(Sections.name == section_name).first()
    if sub_sections is None:
        return jsonify({'error': 'Section not found'}), 404

    sub_sections_choices = [
        (i.name, i.name.capitalize()) for i in sub_sections.sub_sections
    ]
    return jsonify({'sub_sections': sub_sections_choices})


@bp.route('/product-filter', methods=['POST'])
@login_required
def product_filter():
    if not current_user.is_admin:
        return abort(403)
    
    data = request.get_json()
    section_name = data.get('section2')

    if section_name is None:
        return jsonify({'error': 'No section provided'}), 400

    sub_sections = Sections.query.filter(Sections.name == section_name).first()
    if sub_sections is None:
        return jsonify({'error': 'Section not found'}), 404

    sub_sections_choices = [
        (i.name, i.name.capitalize()) for i in sub_sections.sub_sections
    ]
    return jsonify({'sub_sections': sub_sections_choices})
    
    
    
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
    
    form1 = AddSectionsForm()
    form2 = AddSubSectionsForm()
    
    show_sections = Sections.query.all()[::-1]
    sections_for_form = [(i.name, i.name.capitalize()) for i in show_sections]
    form2.select_section.choices.extend(sections_for_form)

    if form1.validate_on_submit() and \
        request.form.get('submit') == 'Add Category':
        sections = Sections()
        try:
            sections.name = form1.name.data.lower()
            db.session.add(sections)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
        
        flash('Категория успешно добавлена!')
        return redirect(url_for('admin.add_sections'))
    
    elif form2.validate_on_submit() and \
        request.form.get('submit') == 'Add SubCategory':
        try:
            section_name = form2.select_section.data.lower()
            sub_section_name = form2.name.data.lower()
            
            section = Sections().query.filter(
                    Sections.name == section_name
            ).first()
            sub_section = SubSections()
            sub_section.name = sub_section_name
            section.sub_sections.append(sub_section)
            db.session.add(section)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
            return redirect(url_for('admin.add_sections'))
        
        flash('Категория успешно добавлена!')
        return redirect(url_for('admin.add_sections'))

    return render_template(
        'admin/add_sections.html',
        show_sections=show_sections,
        form1=form1,
        form2=form2
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
                        product_img = url_for(
                            'static',
                            filename=product.img_link
                        )
                        db.session.delete(product)
                        db.session.commit()
                        delete_product_img(product_img)
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
                        img_paths = map(
                            lambda item: f'/static/img/products/{item.name}',
                            section.sub_sections
                        )
                        db.session.delete(section)
                        db.session.commit()
                        delete_paths_to_img(img_paths)
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                        flash('Не удалось выполнить операцию\nПроверьте корректность вводимых данных!')
                        return redirect(url_for('admin.add_sections'))
                    
            elif what_del == 'subsections':
                sub_section_id = request.form.get('get-id')
                sub_section = SubSections.query.filter(
                    SubSections.id == sub_section_id
                ).first()
                if sub_section:
                    try:
                        section_name = sub_section.name
                        db.session.delete(sub_section)
                        db.session.commit()
                        delete_paths_to_img(
                            [f'/static/img/products/{section_name}']
                        )
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                        flash('Не удалось выполнить операцию\nПроверьте корректность вводимых данных!')
                        return redirect(url_for('admin.add_sections'))        
            
            flash("Удаление выполнено успешно!")
            if what_del == 'sections' or what_del == 'subsections':
                return redirect(url_for('admin.add_sections'))
            return redirect(url_for('admin.admin'))
        
        flash('Перед удалением отметьте подтверждение!')
        if what_del == 'sections' or what_del == 'subsections':
            return redirect(url_for('admin.add_sections'))
        return redirect(url_for('admin.admin'))   
             
    return abort(403)


@bp.route('/custom-update-sections', methods=['POST'])
@login_required
def custom_update_sections():
    if current_user.is_admin:
        confirm = request.form.get('confirm')
        what_update = request.form.get('type')
        if request.method == 'POST' and what_update and confirm:
            user_data = {
                'what_update': what_update,
                'id': request.form.get('get-id'),
            }
            user_data_json = json.dumps(user_data)
            response = make_response(
                render_template('admin/update_sections.html')
            )
            response.set_cookie(
                'user_data',
                user_data_json,
                max_age=60*60*24,
                httponly=True
            )
            return response
        
        elif request.method == 'POST' and confirm:
            user_data_json = request.cookies.get('user_data')
            if user_data_json:
                user_data = json.loads(user_data_json)
                if user_data['what_update'] == 'sections':
                    db_section = Sections.query.filter(
                        Sections.id == user_data['id']
                    ).first()
                    try:
                        db_section.name = request.form.get('name').lower()
                        db.session.add(db_section)
                        db.session.commit()
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                    
                elif user_data['what_update'] == 'subsections':
                    db_sub_section = SubSections.query.filter(
                        SubSections.id == user_data['id']
                    ).first()
                    try:
                        db_sub_section.name = request.form.get('name').lower()
                        db.session.add(db_sub_section)
                        db.session.commit()
                    except Exception as err:
                        db.session.rollback()
                        print(err)
                    
                response = make_response(
                    redirect(url_for('admin.add_sections'))
                )
                response.delete_cookie('user_data')
                return response
            
            return abort(500)
        
        flash('Перед редактированием отметьте кнопку подтверждения!')
        return redirect(url_for('admin.add_sections'))
            
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
    