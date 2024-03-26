from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from .db import db
from .models import Category, Advertisement

views = Blueprint("views", __name__)
from werkzeug.security import generate_password_hash, check_password_hash


def get_random_categories(num_categories=4):
    random_categories = []
    categories = Category.query.order_by(func.random()).limit(num_categories).all()
    for category in categories:
        if category not in random_categories:
            random_categories.append(category)
    return random_categories

def best_categories(num_categories=4):
    best_categories = []

    category_counts = db.session.query(Advertisement.category, func.count(Advertisement.category).label('count')).group_by(Advertisement.category).all()
    sorted_categories = sorted(category_counts, key=lambda x: x[1], reverse=True)
    most_common_categories = sorted_categories[:num_categories]
    for category, _ in most_common_categories:
        category_obj = Category.query.filter_by(name=category).first()
        if category_obj:
            best_categories.append(category_obj)
    while len(best_categories) < num_categories:
        random_category = Category.query.order_by(func.random()).first()
        if random_category and random_category not in best_categories:
            best_categories.append(random_category)

    return best_categories



@views.route("/")
def home():
    categories = best_categories()
    return render_template("home.html", best_categories=categories)


@views.route("/profil")
@login_required
def adatlap():
    return render_template("profile.html", user=current_user)


@views.route("/jelszokezeles", methods=["GET", "PUT", "POST"])
@login_required
def password():
    user = current_user
    if request.method == "POST" or (
        request.method == "GET" and request.args.get("_method") == "PUT"):
        curpassw = request.form.get("curPassw")
        if check_password_hash(user.password, curpassw):
            newpassw1 = request.form.get("newPassw1")
            newpassw2 = request.form.get("newPassw2")
            if not newpassw1 and not newpassw2:
                flash("Az új jelszó mezők nem lehetnek üresek!", category="error")
            elif newpassw1 == newpassw2:
                if curpassw == newpassw1:
                    flash("A jelenlegi és az új jelszó megegyezik!", category="error")
                elif len(newpassw1) < 6:
                    flash("Az új jelszó túl rövid!", category="error")
                else:
                    user.password = generate_password_hash(
                        newpassw1, method="pbkdf2:sha256")
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

@views.route("/adatvedelmi_szabalyzat")
def privacy_policy():
    return render_template("privacy_policy.html")