from flask import Blueprint,render_template, request, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Advertisement, engine, Category, User
from flask_login import current_user
from .db import db
from flask_login import login_required, current_user

hirdetes = Blueprint('hirdetes', __name__)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

@hirdetes.route("/hirdetesek", methods=["GET", "POST"])
def index():
    orderBy = request.form.get("orderBy")
    order = request.form.get("order")

    if request.method == "POST":
        if orderBy == "Ár":
            if order == "Csökkenő":
                sorted_advertisements = Advertisement.query.order_by(Advertisement.price.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = Advertisement.query.order_by(Advertisement.price.asc()).all()

        elif orderBy == "Dátum":
            if order == "Csökkenő":
                sorted_advertisements = Advertisement.query.order_by(Advertisement.date.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = Advertisement.query.order_by(Advertisement.date.asc()).all()

        return sorted_advertisements

    advertisements=Advertisement.query.all()
    return advertisements


@hirdetes.route("/<category>", methods=["GET", "POST"])
def query():
    min = 0
    max = 5000000
    order = 'Csökkenő'
    orderBy = 'Dátum'
    if request.method == "POST":
        min = request.form.get('min')
        max = request.form.get('max')
        order = request.form.get('order')
        orderBy = request.form.get('orderBy')
        category = request.form.get('category')
        # szűrés felhasználó által megadott ár alapján 
        query = session.query(Advertisement).filter_by(category=category)
        done = False
        if min is not None:
            query = query.filter(Advertisement.price >= min)
            done = True
        elif max is not None:
            query = query.filter(Advertisement.price <= max)
            done = True
        if done:
            filtered_advertisements = query.all()
            return filtered_advertisements
        
        # szűrés a felhasználótól sorba rendezés alapján adott kategóriában
        if orderBy == "Ár":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.price.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.price.asc()).all()
            
        elif orderBy == "Dátum":
            if order == "Csökkenő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.date.desc()).all()
            elif order == "Növekvő":
                sorted_advertisements = session.query(Advertisement).filter_by(category=category).order_by(Advertisement.date.asc()).all()
        return sorted_advertisements
    
    # redirecteket MEG KELL CSINÁLNI
            
    # összes hirdetés egy adott kategóriában
    filtered_advertisements = session.query(Advertisement).filter_by(category=category).all()
    return 'ez az összes hardver', filtered_advertisements

@hirdetes.route('/hirdetesfeladas', methods=['GET','POST'])
@login_required
def ujhirdetes():
    if request.method == 'POST':
        title = request.form.get('title')
        category_name = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        userID = current_user.get_id()

        if len(title) < 5 or len(description) < 10 or not price.isdigit() or int(price) < 0:
            flash('Hiba a hirdetés feladásakor.', category='error')
        else:
            newAdv = Advertisement(userID=userID, title=title, category=category_name, description=description, price=int(price))
            db.session.add(newAdv)
            db.session.commit()
            flash('Hirdetés sikeresen feladva!', category='success')

        return redirect(url_for('views.home'))
    else:
        categories = Category.query.all()
        return render_template('new_adv.html', categories=categories)
