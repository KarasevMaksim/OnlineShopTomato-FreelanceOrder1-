from flask import render_template, url_for, request, jsonify
import sqlalchemy as sa
from app.models import Products, Sections, SubSections
from app.main import bp
from app.main.forms import (
    ShowProductsForm
)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = ShowProductsForm()
    sections_item = Sections.query.all()
    sections = [(i.name, i.name.capitalize()) for i in sections_item]
    if sections_item:
        sub_sections = [
            (i.name, i.name.capitalize()) for i in sections_item[0].sub_sections
        ]
        form.select_section2.choices.extend(sections)
        form.select_sub_section2.choices.extend(sub_sections)
    title = 'Tomato'
    products = Products.query.all()[::-1]
    return render_template(
        'index.html',
        title=title,
        products=products,
        form=form
    )

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
    