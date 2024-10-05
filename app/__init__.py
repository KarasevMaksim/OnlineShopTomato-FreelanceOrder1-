from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'admin.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # registration blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.slug import bp as slug_bp
    app.register_blueprint(slug_bp)

    from app.basket import bp as basket_bp
    app.register_blueprint(basket_bp)
    
    from app.news import bp as news_bp
    app.register_blueprint(news_bp)
    
    return app


from app import models
