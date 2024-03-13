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
    if request.method == "POST":
        date_sort = request.form['dateSort']
        price_sort = request.form['priceSort']
        query = Advertisement.query
        if date_sort == 'asc':
            query = query.order_by(Advertisement.date.asc())
        else:
            query = query.order_by(Advertisement.date.desc())
        if price_sort == 'asc':
            query = query.order_by(Advertisement.price.asc())
        else:
            query = query.order_by(Advertisement.price.desc())
        advertisements = query.all()
        return render_template('index.html', advertisements=advertisements)
    # összes hirdetés rendezés nélkül
    advertisements=Advertisement.query.all()
    return render_template("index.html", advertisements=advertisements)


@hirdetes.route("/<category>", methods=["GET", "POST"])
def query(category):
    if request.method == "POST":
        date_sort = request.form['dateSort']
        price_sort = request.form['priceSort']
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        filtered_categories = Category.query.filter_by(main_category=category).all()
        if not filtered_categories:
            filtered_categories = Category.query.filter_by(endpoint_name=category).all()

        advertisements = Advertisement.query.filter(Advertisement.category.in_([cat.name for cat in filtered_categories]))

        # Árszűrés
        if min_price and max_price and min_price <= max_price:
            advertisements = advertisements.filter(Advertisement.price.between(min_price, max_price))
        elif min_price:
            advertisements = advertisements.filter(Advertisement.price >= min_price)
        elif max_price:
            advertisements = advertisements.filter(Advertisement.price <= max_price)

        # Rendezés
        if date_sort == 'asc':
            advertisements = advertisements.order_by(Advertisement.date.asc())
        else:
            advertisements = advertisements.order_by(Advertisement.date.desc())

        if price_sort == 'asc':
            advertisements = advertisements.order_by(Advertisement.price.asc())
        else:
            advertisements = advertisements.order_by(Advertisement.price.desc())

        advertisements = advertisements.all()
        return render_template('adv_by_category.html', filtered_advertisements=advertisements, category=category)

            
    # összes hirdetés egy fő kategóriában
    filtered_categories = Category.query.filter_by(main_category=category).all()

    if not filtered_categories:
        filtered_categories = Category.query.filter_by(endpoint_name=category).all()
    if filtered_categories:
        all_advertisements = Advertisement.query.filter(Advertisement.category.in_([cat.name for cat in filtered_categories])).all()
        if all_advertisements:
            return render_template('adv_by_category.html', filtered_advertisements=all_advertisements, category=category)
        else:
            flash('Nincs hirdetés a kiválasztott kategóriában.', category='error')
    else:
        flash('A kiválasztott kategória nem található.', category='error')
    return redirect(url_for('views.home'))




# 1 hirdetés megjelenítése
@hirdetes.route('/<int:id>', methods=['GET'])
def adv_details(id):
    advertisement = Advertisement.query.get(id)
    if advertisement:
        if current_user.is_authenticated and advertisement.userID == current_user.get_id():
            editable = True
            return render_template('advertisement.html', advertisement=advertisement, editable=editable, userID = current_user.get_id())
        else:
            editable = False
            return render_template('advertisement.html', advertisement=advertisement, userID = current_user.get_id())
    else:
        flash('Nem található ilyen hirdetés', category='error')
        return redirect(url_for('hirdetes.index'))
    


@hirdetes.route("//<int:id>/szerkesztes", methods=["GET","POST"])
@login_required
def adv_edit(id):
    advertisement = Advertisement.query.get(id)
    categories = Category.query.all()
    if request.method == "POST":
        image_error = False
        title = request.form.get('title')
        category_name = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
                filename = secure_filename(image.filename)
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    print("A kép sikeresen feltöltve!")
                else:
                    image_error = True
        if len(title) < 5 or len(description) < 10 or not price.isdigit() or int(price) < 0 or image_error == True:
            print("benne")
            flash('Hiba a hirdetés feladásakor.', category='error')
            return render_template('new_adv.html', categories=categories)
        else:
            advertisement.title = title
            advertisement.category = category_name
            advertisement.description = description
            advertisement.price = int(price)
            advertisement.image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            db.session.commit()
            flash('Hirdetés sikeresen szerkesztve!', category='success')
            return redirect(url_for('views.home'))
    else:
        categories = Category.query.all()
        return render_template('adv_edit.html', advertisement=advertisement, categories=categories)

    



@hirdetes.route("/sajathirdetesek", methods=['GET'])
@login_required
def ownAdv_details():
    advertisements = Advertisement.query.filter_by(userID=current_user.get_id()).all()
    return render_template('index.html', advertisements=advertisements)





@hirdetes.route('/hirdetesfeladas', methods=['GET','POST'])
@login_required
def ujhirdetes():
    image_error = False
    if request.method == 'POST':
        title = request.form.get('title')
        category_name = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        userID = current_user.get_id()
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
                filename = secure_filename(image.filename)
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    print("A kép sikeresen feltöltve!")
                else:
                    image_error = True
        
        if len(title) < 5 or len(description) < 10 or not price.isdigit() or int(price) < 0 or image_error == True:
            print("benne")
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
        hardver_categories = Category.query.filter_by(main_category='hardver').all()
        notebook_categories = Category.query.filter_by(main_category='notebook').all()
        mobil_categories = Category.query.filter_by(main_category='mobil').all()
        
        return render_template('new_adv.html', hardver_categories=hardver_categories, notebook_categories = notebook_categories, mobil_categories = mobil_categories)