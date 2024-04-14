from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Advertisement, engine, Category, User
from flask_login import current_user
from .db import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

hirdetes = Blueprint("hirdetes", __name__)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()

#pagináció globális beállítása
adv_per_page = 5

@hirdetes.route("/", methods=["GET", "POST"])
def index():
    
    
    print('index belep')
    page = int(request.args.get("page", 1))
    offset = (page - 1) * adv_per_page
    sortBy = request.args.get("sortBy", "date_desc")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    advertisements = Advertisement.query

    # Szűrés ár szerint
    if request.method == "POST":
        
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        sortBy = request.form.get("sortBy")
        
        params = {'page': page, 'sortBy': sortBy}
        if min_price:
            params['min_price'] = min_price
        if max_price:
            params['max_price'] = max_price
            
        return redirect(url_for('hirdetes.index', **params))

    if min_price and max_price:
            advertisements = advertisements.filter(Advertisement.price.between(int(min_price), int(max_price)))
    elif min_price:
        advertisements = advertisements.filter(Advertisement.price >= int(min_price))
    elif max_price:
        advertisements = advertisements.filter(Advertisement.price <= int(max_price))

    # Sorrendezés
    if sortBy == "price_desc":
        advertisements = advertisements.order_by(Advertisement.price.desc())
    elif sortBy == "price_asc":
        advertisements = advertisements.order_by(Advertisement.price.asc())
    elif sortBy == "date_desc":
        advertisements = advertisements.order_by(Advertisement.date.desc())
    elif sortBy == "date_asc":
        advertisements = advertisements.order_by(Advertisement.date.asc())

    # Oldalszámozás
    number_of_advs = advertisements.count()
    number_of_pag_pages = -(-number_of_advs // adv_per_page)
    advertisements = advertisements.limit(adv_per_page).offset(offset)

    return render_template(
        "index.html",
        advertisements=advertisements,
        current_page=page,
        number_of_pag_pages=number_of_pag_pages,
        sortBy=sortBy,
        min_price=min_price,
        max_price=max_price,
        advertisementsTypeText = "Összes hirdetés"
    )

@hirdetes.route("/kereses", methods=["GET", "POST"])
def search():
    
    search_term= request.args.get("search_term")
    print(search_term)
    page = int(request.args.get("page", 1))
    offset = (page - 1) * adv_per_page
    sortBy = request.args.get("sortBy", "date_desc")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    advertisements = Advertisement.query
    

    # Szűrés ár szerint
    if request.method == "POST":
        
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        sortBy = request.form.get("sortBy")
        search_term = request.form.get("search_term")
        
        params = {'page': page, 'sortBy': sortBy}
        if min_price:
            params['min_price'] = min_price
        if max_price:
            params['max_price'] = max_price
            
        return redirect(url_for('hirdetes.search', search_term=search_term ,**params))
    
    advertisements = Advertisement.query.filter(
        Advertisement.title.like(f"%{search_term}%"))

    if min_price and max_price:
            advertisements = advertisements.filter(Advertisement.price.between(int(min_price), int(max_price)))
    elif min_price:
        advertisements = advertisements.filter(Advertisement.price >= int(min_price))
    elif max_price:
        advertisements = advertisements.filter(Advertisement.price <= int(max_price))

    # Sorrendezés
    if sortBy == "price_desc":
        advertisements = advertisements.order_by(Advertisement.price.desc())
    elif sortBy == "price_asc":
        advertisements = advertisements.order_by(Advertisement.price.asc())
    elif sortBy == "date_desc":
        advertisements = advertisements.order_by(Advertisement.date.desc())
    elif sortBy == "date_asc":
        advertisements = advertisements.order_by(Advertisement.date.asc())

    # Oldalszámozás
    number_of_advs = advertisements.count()
    number_of_pag_pages = -(-number_of_advs // adv_per_page)
    advertisements = advertisements.limit(adv_per_page).offset(offset)
    
    

    return render_template(
        "index.html",
        advertisements=advertisements,
        current_page=page,
        number_of_pag_pages=number_of_pag_pages,
        sortBy=sortBy,
        min_price=min_price,
        max_price=max_price,
        search_term = search_term,
        advertisementsTypeText = f"Találatok a következőre: "+ search_term
    )

@hirdetes.route("/<category>", methods=["GET", "POST"])
def query(category):
    
    endpoint_category = category
    
    print('category belep')
    page = int(request.args.get("page", 1))
    offset = (page - 1) * adv_per_page
    sortBy = request.args.get("sortBy", "date_desc")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    
    cat_name = "" + category
    full_cat = Category.query.filter(Category.endpoint_name == cat_name).first()
    if full_cat:
        name = full_cat.name
    else:
        name = cat_name[0].upper() + cat_name[1:]

    print("category vár POSTra")
    if request.method == "POST":
        
        print("category POST")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        sortBy = request.form.get("sortBy")
        
        params = {'page': page, 'sortBy': sortBy}
        
        if min_price:
            params['min_price'] = min_price
        if max_price:
            params['max_price'] = max_price
            
            
        return redirect(url_for('hirdetes.query', category=endpoint_category,**params))
    
    

    filtered_categories = Category.query.filter_by(main_category=category).all()
    if not filtered_categories:
        filtered_categories = Category.query.filter_by(endpoint_name=category).all()

    advertisements = Advertisement.query.filter(
        Advertisement.category.in_([cat.name for cat in filtered_categories])
    )

    if min_price and max_price:
            advertisements = advertisements.filter(Advertisement.price.between(int(min_price), int(max_price)))
    elif min_price:
        advertisements = advertisements.filter(Advertisement.price >= int(min_price))
    elif max_price:
        advertisements = advertisements.filter(Advertisement.price <= int(max_price))

    # Sorrendezés
    if sortBy == "price_desc":
        advertisements = advertisements.order_by(Advertisement.price.desc())
    elif sortBy == "price_asc":
        advertisements = advertisements.order_by(Advertisement.price.asc())
    elif sortBy == "date_desc":
        advertisements = advertisements.order_by(Advertisement.date.desc())
    elif sortBy == "date_asc":
        advertisements = advertisements.order_by(Advertisement.date.asc())

    # Oldalszámozás
    number_of_advs = advertisements.count()
    number_of_pag_pages = -(-number_of_advs // adv_per_page)
    advertisements = advertisements.limit(adv_per_page).offset(offset)

    if advertisements.count() > 0:
        print("vannak hirdetesek", advertisements.count())
        return render_template(
        "index.html",
        advertisements=advertisements,
        current_page=page,
        number_of_pag_pages=number_of_pag_pages,
        sortBy=sortBy,
        min_price=min_price,
        max_price=max_price,
        category = endpoint_category,
        advertisementsTypeText = f"Találatok a következőre: "+ category
    )
    else:
        print("nincsenek hirdetesek")
        flash("Nincs hirdetés a kiválasztott kategóriában.", category="error")
        return redirect(url_for("views.home"))


@hirdetes.route("/<int:id>", methods=["GET"])
def adv_details(id):
    advertisement = Advertisement.query.get(id)
    user = current_user
    if advertisement:
        if (
            current_user.is_authenticated
            and advertisement.userID == current_user.get_id()
        ):
            editable = True
            return render_template(
                "advertisement.html",
                advertisement=advertisement,
                editable=editable,
                user=user,
                userID=current_user.get_id(),
            )
        else:
            editable = False
            return render_template(
                "advertisement.html",
                advertisement=advertisement,
                userID=current_user.get_id(),
                user=user,
            )
    else:
        flash("Nem található ilyen hirdetés", category="error")
        return redirect(url_for("hirdetes.index"))


@hirdetes.route("/torles/<int:id>", methods=["POST"])
def adv_delete(id):
    advertisement = Advertisement.query.get(id)
    user = current_user
    if advertisement:
        if (
            current_user.is_authenticated
            and advertisement.userID == current_user.get_id()
        ):
            db.session.delete(advertisement)
            db.session.commit()
            flash("A hirdetésed törlésre került", category="success")
            return redirect(url_for("hirdetes.ownAdv_details"))
        elif user.is_admin:
            db.session.delete(advertisement)
            db.session.commit()
            flash("A hirdetés törlésre került", category="success")
            return redirect(url_for("hirdetes.index"))


@hirdetes.route("/<int:id>/szerkesztes", methods=["GET", "POST"])
@login_required
def adv_edit(id):
    advertisement = Advertisement.query.get(id)
    if request.method == "POST":
        image_error = False
        title = request.form.get("title")
        category_name = request.form.get("category")
        description = request.form.get("description")
        price = request.form.get("price")
        filename = ""
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                allowed_extensions = {"jpg", "jpeg", "png", "gif"}
                filename = secure_filename(image.filename)
                if (
                    "." in filename
                    and filename.rsplit(".", 1)[1].lower() in allowed_extensions
                ):
                    image.save(
                        os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                    )
                else:
                    image_error = True
        if (
            len(title) < 5
            or len(description) < 10
            or not price.isdigit()
            or int(price) < 0
            or image_error == True
            or len(category_name) == 0
            or filename == ""
        ):
            flash("Hiba a hirdetés feladásakor.", category="error")
            hardver_categories = Category.query.filter_by(main_category="hardver").all()
            notebook_categories = Category.query.filter_by(
                main_category="notebook"
            ).all()
            mobil_categories = Category.query.filter_by(main_category="mobil").all()
            return render_template(
                "adv_edit.html",
                advertisement=advertisement,
                hardver_categories=hardver_categories,
                notebook_categories=notebook_categories,
                mobil_categories=mobil_categories,
            )
        else:
            advertisement.title = title
            advertisement.category = category_name
            advertisement.description = description
            advertisement.price = int(price)
            advertisement.image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename
            )
            db.session.commit()
            flash("Hirdetés sikeresen szerkesztve!", category="success")
            return redirect(url_for("views.home"))

    else:
        hardver_categories = Category.query.filter_by(main_category="hardver").all()
        notebook_categories = Category.query.filter_by(main_category="notebook").all()
        mobil_categories = Category.query.filter_by(main_category="mobil").all()
        return render_template(
            "adv_edit.html",
            advertisement=advertisement,
            hardver_categories=hardver_categories,
            notebook_categories=notebook_categories,
            mobil_categories=mobil_categories,
        )


@hirdetes.route("/sajathirdetesek", methods=["GET", "POST"])
@login_required
def userIDadv():
    
    page = int(request.args.get("page", 1))
    offset = (page - 1) * adv_per_page
    sortBy = request.args.get("sortBy", "date_desc")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    advertisements = Advertisement.query
    
    # Szűrés ár szerint
    if request.method == "POST":
        
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        sortBy = request.form.get("sortBy")
        
        
        params = {'page': page, 'sortBy': sortBy}
        if min_price:
            params['min_price'] = min_price
        if max_price:
            params['max_price'] = max_price
            
        return redirect(url_for('hirdetes.userIDadv', **params))
    
    advertisements = Advertisement.query.filter_by(userID=current_user.get_id())
    
    if min_price and max_price:
            advertisements = advertisements.filter(Advertisement.price.between(int(min_price), int(max_price)))
    elif min_price:
        advertisements = advertisements.filter(Advertisement.price >= int(min_price))
    elif max_price:
        advertisements = advertisements.filter(Advertisement.price <= int(max_price))
        
    # Sorrendezés
    if sortBy == "price_desc":
        advertisements = advertisements.order_by(Advertisement.price.desc())
    elif sortBy == "price_asc":
        advertisements = advertisements.order_by(Advertisement.price.asc())
    elif sortBy == "date_desc":
        advertisements = advertisements.order_by(Advertisement.date.desc())
    elif sortBy == "date_asc":
        advertisements = advertisements.order_by(Advertisement.date.asc())
        
    # Oldalszámozás
    number_of_advs = advertisements.count()
    number_of_pag_pages = -(-number_of_advs // adv_per_page)
    advertisements = advertisements.limit(adv_per_page).offset(offset)
    
    
    return render_template(
        "index.html",
        advertisements=advertisements,
        current_page=page,
        number_of_pag_pages=number_of_pag_pages,
        sortBy=sortBy,
        min_price=min_price,
        max_price=max_price,
        advertisementsTypeText = "Saját hirdetéseim"
    )


@hirdetes.route("/felhasznalo=<int:id>", methods=["GET", "POST"])
def advById(id):
    
    page = int(request.args.get("page", 1))
    offset = (page - 1) * adv_per_page
    sortBy = request.args.get("sortBy", "date_desc")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")
    advertisements = Advertisement.query
    
    # Szűrés ár szerint
    if request.method == "POST":
        
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        sortBy = request.form.get("sortBy")
        
        params = {'page': page, 'sortBy': sortBy}
        if min_price:
            params['min_price'] = min_price
        if max_price:
            params['max_price'] = max_price
            
        return redirect(url_for('hirdetes.advById', id = id ,**params))
    
    advertisements = Advertisement.query.filter_by(userID=id)
    
    if min_price and max_price:
            advertisements = advertisements.filter(Advertisement.price.between(int(min_price), int(max_price)))
    elif min_price:
        advertisements = advertisements.filter(Advertisement.price >= int(min_price))
    elif max_price:
        advertisements = advertisements.filter(Advertisement.price <= int(max_price))
        
    # Sorrendezés
    if sortBy == "price_desc":
        advertisements = advertisements.order_by(Advertisement.price.desc())
    elif sortBy == "price_asc":
        advertisements = advertisements.order_by(Advertisement.price.asc())
    elif sortBy == "date_desc":
        advertisements = advertisements.order_by(Advertisement.date.desc())
    elif sortBy == "date_asc":
        advertisements = advertisements.order_by(Advertisement.date.asc())
        
        # Oldalszámozás
    number_of_advs = advertisements.count()
    number_of_pag_pages = -(-number_of_advs // adv_per_page)
    advertisements = advertisements.limit(adv_per_page).offset(offset)
    
    user = User.query.get(id)
    
    return render_template(
        "index.html",
        advertisements=advertisements,
        current_page=page,
        number_of_pag_pages=number_of_pag_pages,
        sortBy=sortBy,
        min_price=min_price,
        max_price=max_price,
        id = id,
        advertisementsTypeText = f"{user.username} hirdetései"
    )
    
    # if request.method == "POST":
    #     sortBy = request.form["sortBy"]
    #     min_price = request.form["min_price"]
    #     max_price = request.form["max_price"]

    #     advertisements = Advertisement.query.filter_by(userID=id)

    #     if min_price and max_price and min_price <= max_price:
    #         advertisements = advertisements.filter(
    #             Advertisement.price.between(min_price, max_price)
    #         )
    #     elif min_price:
    #         advertisements = advertisements.filter(Advertisement.price >= min_price)
    #     elif max_price:
    #         advertisements = advertisements.filter(Advertisement.price <= max_price)

    #     if sortBy == "price_desc":
    #         advertisements = advertisements.order_by(Advertisement.price.desc())
    #     elif sortBy == "price_asc":
    #         advertisements = advertisements.order_by(Advertisement.price.asc())
    #     elif sortBy == "date_desc":
    #         advertisements = advertisements.order_by(Advertisement.date.desc())
    #     elif sortBy == "date_asc":
    #         advertisements = advertisements.order_by(Advertisement.date.asc())

    #     advertisements = advertisements.all()
    #     return render_template("user_adv.html", id=id, advertisements=advertisements)
    # else:
    #     advertisements = Advertisement.query.filter_by(userID=id).all()
    #     return render_template("user_adv.html", id=id, advertisements=advertisements)


@hirdetes.route("/hirdetesfeladas", methods=["GET", "POST"])
@login_required
def ujhirdetes():
    image_error = False

    if request.method == "POST":
        title = request.form.get("title")
        category_name = request.form.get("category")
        description = request.form.get("description")
        price = request.form.get("price")
        userID = current_user.get_id()
        filename = ""
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                allowed_extensions = {"jpg", "jpeg", "png"}
                filename = secure_filename(image.filename)
                base_filename, file_extension = os.path.splitext(filename)

                filename = f"{current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{base_filename}{file_extension}"

                if (
                    "." in filename
                    and filename.rsplit(".", 1)[1].lower() in allowed_extensions
                ):
                    image.save(
                        os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                    )
                else:
                    image_error = True

        error_message = ""
        error = True
        errors = 0
        while error:
            if category_name == None:
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
                flash(error_message, category="error")
                hardver_categories = Category.query.filter_by(
                    main_category="hardver"
                ).all()
                notebook_categories = Category.query.filter_by(
                    main_category="notebook"
                ).all()
                mobil_categories = Category.query.filter_by(main_category="mobil").all()
                return render_template(
                    "new_adv.html",
                    title=title,
                    category=category_name,
                    description=description,
                    price=price,
                    hardver_categories=hardver_categories,
                    notebook_categories=notebook_categories,
                    mobil_categories=mobil_categories,
                )
            else:
                error = False
                newAdv = Advertisement(
                    userID=userID,
                    title=title,
                    category=category_name,
                    description=description,
                    price=int(price),
                    image_path=filename,
                )
                db.session.add(newAdv)
                db.session.commit()
                flash("Hirdetés sikeresen feladva!", category="success")
                return redirect(url_for("views.home"))
    else:
        hardver_categories = Category.query.filter_by(main_category="hardver").all()
        notebook_categories = Category.query.filter_by(main_category="notebook").all()
        mobil_categories = Category.query.filter_by(main_category="mobil").all()

        return render_template(
            "new_adv.html",
            hardver_categories=hardver_categories,
            notebook_categories=notebook_categories,
            mobil_categories=mobil_categories,
        )
