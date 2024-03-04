from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .db import db

views = Blueprint("views", __name__)
from werkzeug.security import generate_password_hash, check_password_hash


@views.route("/")
# @login_required
def home():
    return render_template("home.html", user=current_user)


@views.route("/profile")
@login_required
def adatlap():
    return render_template("profile.html", user=current_user)


@views.route("/password", methods=["GET", "PUT"])
@login_required
def password():
    user = current_user
    if request.method == "PUT":
        curpassw = request.form.get("curPassw")
        if check_password_hash(user.password, curpassw):
            newpassw1 = request.form.get("newPassw1")
            newpassw2 = request.form.get("newPassw2")
            if newpassw1 == newpassw2:
                if curpassw == newpassw1:
                    flash("A jelenlegi és az új jelszó megegyezik!", category="error")
                else:
                    if len(newpassw1) < 6:
                        flash("Az új jelszó túl rövid!", category="error")
                    else:
                        user.password = generate_password_hash(
                            newpassw1, method="pbkdf2:sha256"
                        )
                        db.session.commit()
                        flash("A jelszavad sikeresen megváltoztattad")
                        return redirect(url_for("views.home"))
            else:
                flash("A megadott jelszavak nem egyeznek", category="error")
        else:
            flash("Hibás jelszó", category="error")
    return render_template("profile_passw.html", user=current_user)


@views.route("/aboutus")
def aboutus():
    return render_template("about.html")
