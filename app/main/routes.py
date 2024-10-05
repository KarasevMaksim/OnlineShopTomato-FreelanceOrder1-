import json
from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
import sqlalchemy as sa
from app.models import (
    Products, Sections, SubSections, Contacts, About, SellAndBy
)
from app.main import bp
from app.main.forms import (
    ShowProductsForm, SearchForm, ContactMessageForm
)


@bp.route('/', methods=['GET', 'POST'])
def index():
    title = 'Tomato'
    form = ShowProductsForm()
    form2 = SearchForm()
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
        section_name = user_data['sections']
        sub_section_name = user_data['sub_sections']
        sub_sect = SubSections.query.filter(
            SubSections.name == sub_section_name 
        ).first()
        offset = 0
        products = sub_sect.products[::-1]
        products = products[offset:offset+9]

        if sections_item:
            del_item = (section_name, section_name.capitalize())
            index_del_item = form.select_section2.choices.index(del_item)
            item = form.select_section2.choices.pop(index_del_item)
            form.select_section2.choices.insert(0, item)

            for_sub_item = Sections.query.filter(
                Sections.name == section_name 
            ).first()
            sub_sections = [
            (i.name, i.name.capitalize()) for i in for_sub_item.sub_sections
            ]
            form.select_sub_section2.choices.clear()
            form.select_sub_section2.choices.extend(sub_sections)
            del_sub_item = (sub_section_name, sub_section_name.capitalize())
            index_del_sub_item = form.select_sub_section2.choices.index(
                del_sub_item
            )
            sub_item = form.select_sub_section2.choices.pop(index_del_sub_item)
            form.select_sub_section2.choices.insert(0, sub_item)
    else:
        offset = 0
        products = Products.query.all()[::-1]
        products = products[offset:offset+9]
    
        
    return render_template(
        'index.html',
        title=title,
        form=form,
        form2=form2,
        products=products
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
    

@bp.route('/load-more', methods=['POST'])
def load_more():
    json_cook = request.cookies.get('user_data')
    offset = int(request.form.get('offset', 9))
    limit = 9  # Количество элементов для загрузки за раз
    if json_cook:
        cook = json.loads(json_cook)
        subsection = cook['sub_sections']
        sec = SubSections.query.filter(SubSections.name == subsection).first()
        products = sec.products[::-1]
        products = products[offset:offset+limit]
    else:
        products = Products.query.all()[::-1]
        products = products[offset:offset+9]
    
    return render_template("item_list.html", products=products, offset=offset)


@bp.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_name = form.input_search.data
        products = Products.query.filter(
            Products.name.contains(search_name)
        ).all()
        if not products:
            flash('Не чего не найдено!')
    return render_template('search.html',
                           form=form,
                           products=products
    )

    
@bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactMessageForm()
    contacts = Contacts.query.first()
    
    if form.validate_on_submit():
        return redirect(url_for('main.contacts'))

    return render_template(
        'contacts.html',
        contacts=contacts,
        form=form
    )

    
@bp.route('/more-info')
def more_info():
    about = About.query.first()
    return render_template(
        'more_info.html',
        about=about
    )
    

@bp.route('/sell-and-by')
def sell_and_by():
    sell_and_by = SellAndBy.query.first()
    return render_template(
        'sell_and_by.html',
        sell_and_by=sell_and_by
    )
