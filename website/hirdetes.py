from flask import Blueprint,render_template, request, flash, redirect, url_for, current_app
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Advertisement, engine, Category, User
from flask_login import current_user
from .db import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

hirdetes = Blueprint('hirdetes', __name__)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()


@hirdetes.route("/osszes", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sortBy = request.form['sortBy']
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        advertisements = Advertisement.query

        if min_price and max_price and min_price <= max_price:
            advertisements = advertisements.filter(Advertisement.price.between(min_price, max_price))
        elif min_price:
            advertisements = advertisements.filter(Advertisement.price >= min_price)
        elif max_price:
            advertisements = advertisements.filter(Advertisement.price <= max_price)

        if sortBy == 'price_desc':
            advertisements = advertisements.order_by(Advertisement.price.desc())
        elif sortBy == 'price_asc':
            advertisements = advertisements.order_by(Advertisement.price.asc())
        elif sortBy == 'date_desc':
            advertisements = advertisements.order_by(Advertisement.date.desc())
        elif sortBy == 'date_asc':
            advertisements = advertisements.order_by(Advertisement.date.asc())

        advertisements = advertisements.all()
        return render_template('index.html', advertisements=advertisements)
    else:
        advertisements = Advertisement.query.all()
        return render_template("index.html", advertisements=advertisements)




@hirdetes.route("/<category>", methods=["GET", "POST"])
def query(category):
    cat_name = "" + category
    full_cat = Category.query.filter(Category.endpoint_name == cat_name).first()
    if full_cat:
        name = full_cat.name
    else:
        name = cat_name[0].upper() + cat_name[1:]
    print(name)

    if request.method == "POST":
        sortBy = request.form['sortBy']
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
        if sortBy == 'price_desc':
            advertisements = advertisements.order_by(Advertisement.price.desc())
        elif sortBy == 'price_asc':
            advertisements = advertisements.order_by(Advertisement.price.asc())
        elif sortBy == 'date_desc':
            advertisements = advertisements.order_by(Advertisement.date.desc())
        elif sortBy == 'date_asc':
            advertisements = advertisements.order_by(Advertisement.date.asc())

        advertisements = advertisements.all()
        return render_template('adv_by_category.html', filtered_advertisements=advertisements, category=category, name=name)

            
    # összes hirdetés egy fő kategóriában
    filtered_categories = Category.query.filter_by(main_category=category).all()

    if not filtered_categories:
        filtered_categories = Category.query.filter_by(endpoint_name=category).all()
    if filtered_categories:
        all_advertisements = Advertisement.query.filter(Advertisement.category.in_([cat.name for cat in filtered_categories])).all()
        if all_advertisements:
            return render_template('adv_by_category.html', filtered_advertisements=all_advertisements, category=category, name=name)
        else:
            flash('Nincs hirdetés a kiválasztott kategóriában.', category='error')
    else:
        flash('A kiválasztott kategória nem található.', category='error')
    return redirect(url_for('views.home'))



@hirdetes.route('/<int:id>', methods=['GET'])
def adv_details(id):
    advertisement = Advertisement.query.get(id)
    user = current_user
    if advertisement:
        if current_user.is_authenticated and advertisement.userID == current_user.get_id():
            editable = True
            return render_template('advertisement.html', advertisement=advertisement, editable=editable, user=user, userID=current_user.get_id())
        else:
            editable = False
            return render_template('advertisement.html', advertisement=advertisement, userID=current_user.get_id(), user=user)
    else:
        flash('Nem található ilyen hirdetés', category='error')
        return redirect(url_for('hirdetes.index'))
    


@hirdetes.route('/torles/<int:id>', methods=['POST'])
def adv_delete(id):
    advertisement = Advertisement.query.get(id)
    user = current_user
    if advertisement:
        if current_user.is_authenticated and advertisement.userID == current_user.get_id():
            db.session.delete(advertisement)
            db.session.commit()
            flash('A hirdetésed törlésre került', category='success')
            return redirect(url_for('hirdetes.ownAdv_details'))
        elif user.is_admin:
            db.session.delete(advertisement)
            db.session.commit()
            flash('A hirdetés törlésre került', category='success')
            return redirect(url_for('hirdetes.index'))



@hirdetes.route("//<int:id>/szerkesztes", methods=["GET","POST"])
@login_required
def adv_edit(id):
    advertisement = Advertisement.query.get(id)
    if request.method == "POST":
        image_error = False
        title = request.form.get('title')
        category_name = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        filename = ""
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
                filename = secure_filename(image.filename)
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                else:
                    image_error = True
        
        error_message = ""
        error = True
        errors = 0

        while error:
            if len(category_name) == 0:
                error_message = "Válasszon kategóriát!"
                errors += 1

            if not price.isdigit() or int(price) < 0:
                error_message = "Nem megfelelő ár formátum!"
                errors += 1

            if len(description) < 10:
                error_message = "A hírdetés leírása kevesebb mint 10 karakter!"
                errors += 1
            elif len(description) > 1000:
                error_message = "A hírdetés leírása több mint 10 karakter!"
                errors += 1

            if len(title) < 5:
                error_message = "A hírdetés címe kevesebb mint 5 karakter!"
                errors += 1
            elif len(title) > 60:
                error_message = "A hírdetés címe hosszabb mint 60 karakter!"
                errors += 1

            if image_error:
                error_message = "Nem megfelelő kiterjesztés!"
                errors += 1
            if filename == "":
                error_message = "Nem töltött fel képet!"
                errors += 1

            if errors > 0:
                flash(error_message, category='error')
                hardver_categories = Category.query.filter_by(main_category='hardver').all()
                notebook_categories = Category.query.filter_by(main_category='notebook').all()
                mobil_categories = Category.query.filter_by(main_category='mobil').all()
                return render_template('adv_edit.html', advertisement=advertisement, hardver_categories=hardver_categories, notebook_categories = notebook_categories, mobil_categories = mobil_categories)
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
        hardver_categories = Category.query.filter_by(main_category='hardver').all()
        notebook_categories = Category.query.filter_by(main_category='notebook').all()
        mobil_categories = Category.query.filter_by(main_category='mobil').all()
        return render_template('adv_edit.html', advertisement=advertisement, hardver_categories=hardver_categories, notebook_categories = notebook_categories, mobil_categories = mobil_categories)

    



@hirdetes.route("/sajathirdetesek", methods=['GET', 'POST'])
@login_required
def ownAdv_details():
    if request.method == "POST":
        sortBy = request.form['sortBy']
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        advertisements = Advertisement.query.filter_by(userID=current_user.get_id())

        if min_price and max_price and min_price <= max_price:
            advertisements = advertisements.filter(Advertisement.price.between(min_price, max_price))
        elif min_price:
            advertisements = advertisements.filter(Advertisement.price >= min_price)
        elif max_price:
            advertisements = advertisements.filter(Advertisement.price <= max_price)

        if sortBy == 'price_desc':
            advertisements = advertisements.order_by(Advertisement.price.desc())
        elif sortBy == 'price_asc':
            advertisements = advertisements.order_by(Advertisement.price.asc())
        elif sortBy == 'date_desc':
            advertisements = advertisements.order_by(Advertisement.date.desc())
        elif sortBy == 'date_asc':
            advertisements = advertisements.order_by(Advertisement.date.asc())

        advertisements = advertisements.all()
        return render_template('own_adv.html', advertisements=advertisements)
    else:
        advertisements = Advertisement.query.filter_by(userID=current_user.get_id()).all()
        return render_template('own_adv.html', advertisements=advertisements)
    




@hirdetes.route("/felhasznalo=<int:id>")
def advByUser(id):
    if request.method == "POST":
        sortBy = request.form['sortBy']
        min_price = request.form['min_price']
        max_price = request.form['max_price']

        advertisements = Advertisement.query.filter_by(userID=id)

        if min_price and max_price and min_price <= max_price:
            advertisements = advertisements.filter(Advertisement.price.between(min_price, max_price))
        elif min_price:
            advertisements = advertisements.filter(Advertisement.price >= min_price)
        elif max_price:
            advertisements = advertisements.filter(Advertisement.price <= max_price)

        if sortBy == 'price_desc':
            advertisements = advertisements.order_by(Advertisement.price.desc())
        elif sortBy == 'price_asc':
            advertisements = advertisements.order_by(Advertisement.price.asc())
        elif sortBy == 'date_desc':
            advertisements = advertisements.order_by(Advertisement.date.desc())
        elif sortBy == 'date_asc':
            advertisements = advertisements.order_by(Advertisement.date.asc())

        advertisements = advertisements.all()
        return render_template('user_adv.html', id=id, advertisements=advertisements)
    else:
        advertisements = Advertisement.query.filter_by(userID=id).all()
        return render_template('user_adv.html', id=id, advertisements=advertisements)





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
        filename = ""
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                allowed_extensions = {'jpg', 'jpeg', 'png'}
                filename = secure_filename(image.filename)
                base_filename, file_extension = os.path.splitext(filename)
                
                filename = f"{current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{base_filename}{file_extension}"
                
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                else:
                    image_error = True
        
        error_message = ""
        error = True
        errors = 0

        while error:
            if len(category_name) == 0:
                error_message = "Válasszon kategóriát!"
                category_name = "Válasszon kategóriát"
                errors += 1

            if not price.isdigit() or int(price) < 0:
                error_message = "Nem megfelelő ár formátum!"
                errors += 1

            if len(description) < 10:
                error_message = "A hírdetés leírása kevesebb mint 10 karakter!"
                errors += 1
            elif len(description) > 1000:
                error_message = "A hírdetés leírása több mint 10 karakter!"
                errors += 1

            if len(title) < 5:
                error_message = "A hírdetés címe kevesebb mint 5 karakter!"
                errors += 1
            elif len(title) > 60:
                error_message = "A hírdetés címe hosszabb mint 60 karakter!"
                errors += 1

            if image_error:
                error_message = "Nem megfelelő kiterjesztés!"
                errors += 1
            if filename == "":
                error_message = "Nem töltött fel képet!"
                errors += 1

            if errors > 0:
                flash(error_message, category='error')
                hardver_categories = Category.query.filter_by(main_category='hardver').all()
                notebook_categories = Category.query.filter_by(main_category='notebook').all()
                mobil_categories = Category.query.filter_by(main_category='mobil').all()
                return render_template('new_adv.html',title=title, category=category_name, description=description, price=price, hardver_categories=hardver_categories, notebook_categories = notebook_categories, mobil_categories = mobil_categories)
            else:
                error = False
                newAdv = Advertisement(userID=userID, title=title, category=category_name, description=description, price=int(price), image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                db.session.add(newAdv)
                db.session.commit()
                flash('Hirdetés sikeresen feladva!', category='success')
                return redirect(url_for('views.home'))
    else:
        category_name = "Válasszon kategóriát!"
        hardver_categories = Category.query.filter_by(main_category='hardver').all()
        notebook_categories = Category.query.filter_by(main_category='notebook').all()
        mobil_categories = Category.query.filter_by(main_category='mobil').all()
        
        return render_template('new_adv.html', category=category_name, hardver_categories=hardver_categories, notebook_categories = notebook_categories, mobil_categories = mobil_categories)