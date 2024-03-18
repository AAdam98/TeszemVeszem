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
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{path.join(app.instance_path, DB_NAME)}"
    )
    UPLOAD_FOLDER = "website/uploads"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
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
                    ("hardver", "Alaplap", "icons/alaplap.svg", "alaplap"),
                    ("hardver", "Processzor", "icons/processzor.svg", "processzor"),
                    ("hardver", "Memória", "icons/memoria.svg", "memoria"),
                    ("hardver", "Hűtés", "icons/hutes.svg", "hutes"),
                    ("hardver", "Ház, táp", "icons/haz.svg", "haz_tap"),
                    (
                        "hardver",
                        "Játékvezérlő, szimulátor",
                        "icons/jatekvezerlo.svg",
                        "jatekvezerlo_szimulator",
                    ),
                    ("hardver", "VR", "icons/vr.svg", "vr"),
                    (
                        "hardver",
                        "Billentyűzet, egér(pad)",
                        "icons/billentyuzet.svg",
                        "billentyuzet_eger",
                    ),
                    (
                        "hardver",
                        "Egyéb hardverek",
                        "icons/egyebhardver.svg",
                        "egyeb_hardverek",
                    ),
                    (
                        "hardver",
                        "Retró hardverek",
                        "icons/retrohardver.svg",
                        "retro_hardverek",
                    ),
                    ("hardver", "Videókártya", "icons/videokartya.svg", "videokartya"),
                    ("hardver", "Monitor", "icons/monitor.svg", "monitor"),
                    (
                        "hardver",
                        "Merevlemez, SSD",
                        "icons/merevlemezssd.svg",
                        "merevlemez_ssd",
                    ),
                    ("hardver", "Adathordozó", "icons/adathordozo.svg", "adathordozo"),
                    (
                        "hardver",
                        "Hálózati termékek",
                        "icons/halozati.svg",
                        "halozati_termekek",
                    ),
                    (
                        "hardver",
                        "Nyomtató, szkenner",
                        "icons/nyomtato.svg",
                        "nyomtato_szkenner",
                    ),
                    ("mobil", "IPhone", "icons/mobil.svg", "iphone"),
                    ("mobil", "Samsung", "icons/mobil.svg", "samsung"),
                    ("mobil", "Sony", "icons/mobil.svg", "sony"),
                    ("mobil", "LG", "icons/mobil.svg", "lg"),
                    ("mobil", "Asus", "icons/mobil.svg", "asus"),
                    ("mobil", "Google", "icons/mobil.svg", "google"),
                    (
                        "mobil",
                        "Xiaomi, Redmi, Poco",
                        "icons/mobil.svg",
                        "xiaomi_redmi_poco",
                    ),
                    ("mobil", "Huawei", "icons/mobil.svg", "huawei"),
                    ("mobil", "Honor", "icons/mobil.svg", "honor"),
                    ("mobil", "Realme", "icons/mobil.svg", "realme"),
                    ("mobil", "OnePlus", "icons/mobil.svg", "oneplus"),
                    ("mobil", "Oppo", "icons/mobil.svg", "oppo"),
                    ("mobil", "Nokia", "icons/mobil.svg", "nokia"),
                    ("mobil", "Motorola", "icons/mobil.svg", "motorola"),
                    ("mobil", "Lenovo", "icons/mobil.svg", "lenovo"),
                    ("notebook", "MacBook", "icons/notebook.svg", "macbook"),
                    ("notebook", "MacBook Air", "icons/notebook.svg", "macbook_air"),
                    ("notebook", "MacBook Pro", "icons/notebook.svg", "macbook_pro"),
                    ("notebook", "Subnotebook", "icons/notebook.svg", "subnotebook"),
                    (
                        "notebook",
                        "Könnyű notebook",
                        "icons/notebook.svg",
                        "konnyu_notebook",
                    ),
                    (
                        "notebook",
                        "Asztali notebook",
                        "icons/notebook.svg",
                        "asztali_notebook",
                    ),
                    (
                        "notebook",
                        "Nagyméretű notebook",
                        "icons/notebook.svg",
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