from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models import User, Category
from .db import db
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

DB_NAME= "database.sqlite"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'macskajaj'
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{path.join(app.instance_path, DB_NAME)}'
    db.init_app(app)
    migrate = Migrate(app, db)
    
    
    from .views import views
    from .auth import auth
    from .hirdetes import hirdetes
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')
    app.register_blueprint(hirdetes, url_prefix='/hirdetes/')
    
    from .models import Advertisement, User, Comment
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash('Ehhez az oldalhoz be kell jelentkezned!', 'warning')
        return redirect(url_for('auth.login'))
    
    create_database(app)
    
    return app

def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    if not path.exists(db_path):
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
                categories = ["Alaplap","Processzor","Memória","Hűtés","Ház, táp","Játékvezérlő, szimulátor",
                              "VR", "Billentyűzet, egér(pad)","Egyéb hardverek","Retró hardverek","Videókártya", 
                              "Monitor","Merevlemez, SSD","Adathordozó","Hálózati termékek","Nyomtató, szkenner"]
                for category in categories:
                    newCat = Category(name=category)
                    db.session.add(newCat)
            db.session.commit()
        print('Adatbázis létrehozva!')