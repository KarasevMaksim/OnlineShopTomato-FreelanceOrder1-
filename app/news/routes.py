from flask import (
    render_template, url_for, request, jsonify, make_response, redirect, abort,
    flash
)
from app.models import News
from app.news import bp


@bp.route('/')
def index():
    news = News.query.all()
    print(news[0].post)
    return render_template(
        'news/news.html',
        news=news
    )
    