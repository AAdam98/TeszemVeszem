from flask import Blueprint,render_template, request, flash, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Advertisement, engine, Category, User
from flask_login import current_user
from .db import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

hirdetes = Blueprint('hirdetes', __name__)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()


@hirdetes.route("/osszes", methods=["GET", "POST"])
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
    return render_template("index.html", advertisements=advertisements)


@hirdetes.route("/<category>", methods=["GET", "POST"])
def query(category):
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
    filtered_category = Category.query.filter_by(endpoint_name=category).first()
    name = filtered_category.name
    filtered_advertisements = Advertisement.query.filter_by(category=name).all()
    return render_template('adv_by_category.html', filtered_advertisements=filtered_advertisements)

@hirdetes.route('/<int:id>', methods=['GET','POST'])
def adv_details(id):
    advertisement = Advertisement.query.filter_by(advertisementID=id).first()
    return render_template('advertisement.html', advertisement=advertisement)

@hirdetes.route('/hirdetesfeladas', methods=['GET','POST'])
@login_required
def ujhirdetes():
    
    if request.method == 'POST':
        title = request.form.get('title')
        category_name = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        userID = current_user.get_id()
        print("kezdes")
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                print("benne")
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        print("vege", request.files)

        if len(title) < 5 or len(description) < 10 or not price.isdigit() or int(price) < 0:
            flash('Hiba a hirdetés feladásakor.', category='error')
            categories = Category.query.all()
            return render_template('new_adv.html', categories=categories)
        else:
            newAdv = Advertisement(userID=userID, title=title, category=category_name, description=description, price=int(price), image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            db.session.add(newAdv)
            db.session.commit()
            flash('Hirdetés sikeresen feladva!', category='success')
            return redirect(url_for('views.home'))
    else:
        categories = Category.query.all()
        return render_template('new_adv.html', categories=categories)
