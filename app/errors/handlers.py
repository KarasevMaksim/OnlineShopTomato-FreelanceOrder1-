from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template(
        'errors/error_page.html',
        type_error=404), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'errors/error_page.html',
        type_error=500), 500
    
    
@bp.app_errorhandler(403)
def internal_error(error):
    db.session.rollback()
    return render_template(
        'errors/error_page.html',
        type_error=403), 403