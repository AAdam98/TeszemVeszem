from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager
from .models import User, Category
from .db import db
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate

DB_NAME = "database.sqlite"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "macskajaj"
    app.config["SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{path.join(app.instance_path, DB_NAME)}")
    
    
    UPLOAD_FOLDER = "website/static/cdn"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print("CDN MAPPA LETREHOZVA")
        
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth
    from .hirdetes import hirdetes

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(hirdetes, url_prefix="/hirdetes/")

    from .models import Advertisement, User, Comment

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("Ehhez az oldalhoz be kell jelentkezned!", "warning")
        return redirect(url_for("auth.login"))
    
    @app.context_processor
    def inject_models():
        return dict(User=User)

    create_database(app)


    return app


def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            email = "admin@admin.com"
            username = "admin"
            password = "Admin123"
            user = User.query.filter_by(email=email).first()
            if user:
                pass
            else:
                admin_user = User(
                    email=email,
                    username=username,
                    password=generate_password_hash(password, method="pbkdf2:sha256"),
                    is_admin=True,
                )
                db.session.add(admin_user)

                categories = [
                    ("hardver", "Alaplap", "bi-motherboard", "alaplap"),
                    ("hardver", "Processzor", "bi-cpu", "processzor"),
                    ("hardver", "Memória", "bi-memory", "memoria"),
                    ("hardver", "Hűtés", "bi-fan", "hutes"),
                    ("hardver", "Ház, táp", "bi-pc", "haz_tap"),
                    (
                        "hardver",
                        "Játékvezérlő, szimulátor",
                        "bi-controller",
                        "jatekvezerlo_szimulator",
                    ),
                    ("hardver", "VR", "bi-badge-vr", "vr"),
                    (
                        "hardver",
                        "Billentyűzet, egér(pad)",
                        "bi-keyboard",
                        "billentyuzet_eger",
                    ),
                    (
                        "hardver",
                        "Egyéb hardverek",
                        "bi-pci-card",
                        "egyeb_hardverek",
                    ),
                    (
                        "hardver",
                        "Retró hardverek",
                        "bi-archive",
                        "retro_hardverek",
                    ),
                    ("hardver", "Videókártya", "bi-gpu-card", "videokartya"),
                    ("hardver", "Monitor", "bi-display", "monitor"),
                    (
                        "hardver",
                        "Merevlemez, SSD",
                        "bi-hdd",
                        "merevlemez_ssd",
                    ),
                    ("hardver", "Adathordozó", "bi-sd-card", "adathordozo"),
                    (
                        "hardver",
                        "Hálózati termékek",
                        "bi-router",
                        "halozati_termekek",
                    ),
                    (
                        "hardver",
                        "Nyomtató, szkenner",
                        "bi-printer",
                        "nyomtato_szkenner",
                    ),
                    ("mobil", "IPhone", "bi-phone", "iphone"),
                    ("mobil", "Samsung", "bi-phone", "samsung"),
                    ("mobil", "Sony", "bi-phone", "sony"),
                    ("mobil", "LG", "bi-phone", "lg"),
                    ("mobil", "Asus", "bi-phone", "asus"),
                    ("mobil", "Google", "bi-phone", "google"),
                    (
                        "mobil",
                        "Xiaomi, Redmi, Poco",
                        "bi-phone",
                        "xiaomi_redmi_poco",
                    ),
                    ("mobil", "Huawei", "bi-phone", "huawei"),
                    ("mobil", "Honor", "bi-phone", "honor"),
                    ("mobil", "Realme", "bi-phone", "realme"),
                    ("mobil", "OnePlus", "bi-phone", "oneplus"),
                    ("mobil", "Oppo", "bi-phone", "oppo"),
                    ("mobil", "Nokia", "bi-phone", "nokia"),
                    ("mobil", "Motorola", "bi-phone", "motorola"),
                    ("mobil", "Lenovo", "bi-phone", "lenovo"),
                    ("notebook", "MacBook", "bi-laptop", "macbook"),
                    ("notebook", "MacBook Air", "bi-laptop", "macbook_air"),
                    ("notebook", "MacBook Pro", "bi-laptop", "macbook_pro"),
                    ("notebook", "Subnotebook", "bi-laptop", "subnotebook"),
                    (
                        "notebook",
                        "Könnyű notebook",
                        "bi-laptop",
                        "konnyu_notebook",
                    ),
                    (
                        "notebook",
                        "Asztali notebook",
                        "bi-laptop",
                        "asztali_notebook",
                    ),
                    (
                        "notebook",
                        "Nagyméretű notebook",
                        "bi-laptop",
                        "nagymeretu_notebook",
                    ),
                ]

                for main_category, name, icon_path, endpoint_name in categories:
                    newCat = Category(
                        main_category=main_category,
                        name=name,
                        icon_path=icon_path,
                        endpoint_name=endpoint_name,
                    )
                    db.session.add(newCat)
            db.session.commit()