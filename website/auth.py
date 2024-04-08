from flask import Blueprint, render_template, request, flash, redirect, url_for

auth = Blueprint("auth", __name__)
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Sikeresen bejelentkeztél!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Helytelen jelszó.", category="error")
        else:
            flash("Nincs ilyen e-mail címmel regisztrált felhasználó.", category="error")
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sikeres kijelentkezés!", category="success")
    return redirect(url_for("views.home"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        userName = User.query.filter_by(username=username).first()
        if user:
            flash("Ezzel az e-mail címmel már regisztráltak.", category="error")
        elif userName:
            flash("Ez a felhasználónév már foglalt.", category="error")
        elif len(email) < 3 or not "@" in email or not "." in email:
            flash("Nem megfelelő email cím formátum!", category="error")
        elif len(username) < 4:
            flash("A felhasználónév nem lehet rövidebb mint 4 karakter", category="error")
        elif password1 != password2:
            flash("Nem egyeznek a jelszavak", category="error")
        elif len(password1) < 6:
            flash("Jelszó nem lehet rövidebb mint 6 karakter", category="error")
        else:
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="pbkdf2:sha256")
            )
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            flash("A fiók sikeresen létrehozva.", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)
