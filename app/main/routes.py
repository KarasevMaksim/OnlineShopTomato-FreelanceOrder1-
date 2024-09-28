import json
from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort
)
import sqlalchemy as sa
from app.models import Products, Sections, SubSections
from app.main import bp
from app.main.forms import (
    ShowProductsForm
)


@bp.route('/', methods=['GET', 'POST'])
def index():
    title = 'Tomato'
    form = ShowProductsForm()
    sections_item = Sections.query.all()
    sections = [(i.name, i.name.capitalize()) for i in sections_item]
    if sections_item:
        sub_sections = [
            (i.name, i.name.capitalize()) for i in sections_item[0].sub_sections
        ]
        form.select_section2.choices.extend(sections)
        form.select_sub_section2.choices.extend(sub_sections)
    if request.cookies.get('user_data'):
        user_data = json.loads(request.cookies.get('user_data'))
        sub_sect = SubSections.query.filter(
            SubSections.name == user_data['sub_sections']
        ).first()
        products = sub_sect.products
    else:
        products = Products.query.all()[::-1]
    return render_template(
        'index.html',
        title=title,
        products=products,
        form=form
    )


@bp.route('/update-puduct', methods=['POST'])
def update_product():
    form = ShowProductsForm()
    check_type_button = form.submit1.data
    section = form.select_section2.data
    sub_section = form.select_sub_section2.data

    if section and sub_section and check_type_button:
        user_data = {
            'sections': section,
            'sub_sections': sub_section
        }
        user_data_json = json.dumps(user_data)
        response = make_response(
            redirect(url_for('main.index'))
        )
        response.set_cookie(
            'user_data',
            user_data_json,
            max_age=60*60*24
        )
        return response

    elif request.cookies.get('user_data') and not check_type_button:
        response = make_response(redirect(url_for('main.index')))
        response.delete_cookie('user_data')
        return response

    return redirect(url_for('main.index'))


@bp.route('/product-filter', methods=['POST'])
def product_filter():
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
    