from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db= SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'macskajaj'
    app.config['SQLAlCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .hardver import hardver
    
    #Bliuprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(hardver, url_prefux='/hardver/')
    
    from .models import Advertisement, User, Comment
    
    create_database(app)
    
    return app

def create_database(app):
    if not path('website/' + DB_NAME):
        db.create_all(app=app)
        print('Adatbázis létrehozva!')