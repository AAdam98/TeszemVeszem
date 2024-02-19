from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models import User
from .db import db
from werkzeug.security import generate_password_hash

DB_NAME= "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'macskajaj'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .hardver import hardver
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(hardver, url_prefix='/hardver/')
    
    from .models import Advertisement, User, Comment
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    create_database(app)
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            email = 'admin@admin.com'
            username = 'admin'
            password = 'Admin123'
            user = User.query.filter_by(email=email).first()
            if user:
                pass
            else:
                admin_user = User(email=email, username = username, password=generate_password_hash(password,method='pbkdf2:sha256'), is_admin=True)
                db.session.add(admin_user)
                db.session.commit()
        print('Adatbázis létrehozva!')