from flask import (
    render_template
)
from app.models import News
from app.news import bp


@bp.route('/')
def index():
    news = News.query.all()[::-1]
    print(news[0].post)
    return render_template(
        'news/news.html',
        news=news
    )
    